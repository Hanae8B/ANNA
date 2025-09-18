# core/neural.py
import os
import re
import sympy as sp
import pandas as pd
import numpy as np
from fuzzywuzzy import process
from . import kb_entries
import requests
import feedparser
from sklearn.metrics.pairwise import cosine_similarity

# Optional transformer for semantic search
try:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
    kb_texts = list(kb_entries.kb_entries.values())
    kb_embeddings = model.encode(kb_texts, convert_to_tensor=True)
except ImportError:
    model = None
    kb_embeddings = None

# Contextual memory
memory = {
    "last_query": None,
    "last_result": None
}

def preprocess_query(query: str):
    """
    Extract intent and relevant content from a casual query.
    """
    query_lower = query.lower().strip()

    # Detect calculation intent
    calc_match = re.search(r'((?:\d+[\+\-\*/\^\.]?)+)', query_lower.replace('^', '**'))
    if calc_match:
        return "calculate", calc_match.group(0)

    # Detect derivative or integral
    if "derivative" in query_lower:
        expr = query_lower.replace("derivative of", "").strip()
        return "derivative", expr
    if "integral" in query_lower:
        expr = query_lower.replace("integral of", "").strip()
        return "integral", expr

    # Detect file analysis
    if "analyze file" in query_lower:
        file_path = query_lower.split("analyze file")[-1].strip()
        return "file_analysis", file_path

    # Detect comparison
    if "difference between" in query_lower or "compare" in query_lower:
        subjects = re.findall(r'between (.+?) and (.+)', query_lower)
        if subjects:
            return "comparison", subjects[0]

    # Default: definition / general question
    return "definition", query_lower

def math_layer(intent, content):
    """
    Evaluate mathematical expressions and symbolic operations.
    """
    try:
        if intent == "calculate":
            result = sp.sympify(content).evalf()
            return f"{round(result,6)}"
        elif intent == "derivative":
            result = sp.diff(sp.sympify(content))
            return str(result)
        elif intent == "integral":
            result = sp.integrate(sp.sympify(content))
            return str(result)
    except Exception as e:
        return f"Calculation error: {e}"
    return None

def knowledge_layer(intent, content):
    """
    Return definitions, comparisons, or fuzzy KB matches.
    """
    # Exact or fuzzy KB match
    keys = list(kb_entries.kb_entries.keys())
    if intent == "definition":
        # Fuzzy match
        match, score = process.extractOne(content, [k.lower() for k in keys])
        if score >= 70:
            return kb_entries.kb_entries[keys[[k.lower() for k in keys].index(match)]]
    # Comparison layer
    if intent == "comparison":
        sub1, sub2 = content
        info1 = kb_entries.kb_entries.get(sub1.title(), "")
        info2 = kb_entries.kb_entries.get(sub2.title(), "")
        if info1 and info2:
            return f"{sub1.title()} vs {sub2.title()}:\n- {sub1}: {info1}\n- {sub2}: {info2}\nDifferences: {sub1.title()} and {sub2.title()} have distinct properties."
    return None

def csv_analysis_layer(file_path):
    """
    Analyze CSV file: numeric correlations + categorical counts.
    """
    if not os.path.exists(file_path):
        return f"File not found: {file_path}", None
    try:
        df = pd.read_csv(file_path)
        numeric_cols = df.select_dtypes(include='number').columns
        categorical_cols = df.select_dtypes(exclude='number').columns
        summary_text = f"Data Summary: {df.shape[0]} rows, {df.shape[1]} columns.\n"
        if len(numeric_cols) > 0:
            summary_text += f"Numeric columns: {', '.join(numeric_cols)}\n"
            # Strong correlations
            corr = df[numeric_cols].corr()
            strong_corr = []
            reported = set()
            for i in numeric_cols:
                for j in numeric_cols:
                    if i != j and abs(corr.loc[i,j]) > 0.9 and (j,i) not in reported:
                        strong_corr.append(f"{i} ↔ {j} = {corr.loc[i,j]:.2f}")
                        reported.add((i,j))
            if strong_corr:
                summary_text += "Strong correlations:\n" + "\n".join(strong_corr) + "\n"

        if len(categorical_cols) > 0:
            summary_text += "Categorical column counts:\n"
            for col in categorical_cols:
                counts = df[col].value_counts().to_dict()
                most_common = max(counts, key=counts.get)
                summary_text += f"- {col}: most common = {most_common}, counts = {counts}\n"
        return summary_text, df
    except Exception as e:
        return f"Error reading file: {e}", None

def fallback_layer(query):
    """
    Query online sources like PubMed and arXiv if offline layers fail.
    """
    responses = []

    # PubMed
    try:
        pubmed_url = f"https://api.ncbi.nlm.nih.gov/lit/ctxp/v1/pubmed/?format=citation&term={query}"
        resp = requests.get(pubmed_url, timeout=5)
        if resp.status_code == 200 and resp.text.strip():
            responses.append(f"Check PubMed for research articles: {pubmed_url}")
    except:
        pass

    # arXiv
    try:
        arxiv_url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=3"
        feed = feedparser.parse(arxiv_url)
        if feed.entries:
            arxiv_entries = []
            for entry in feed.entries:
                title = entry.title
                summary = entry.summary.replace('\n',' ')
                link = entry.link
                arxiv_entries.append(f"Title: {title}\nSummary: {summary}\nLink: {link}")
            responses.append("\n--- arXiv Papers ---\n" + "\n".join(arxiv_entries))
    except:
        pass

    return "\n".join(responses) if responses else "ANNA could not find a direct offline explanation. Please consult peer-reviewed scientific literature."

def reason(query: str):
    """
    Main brain function: orchestrates all layers.
    Returns text response and optional DataFrame for plots.
    """
    global memory
    intent, content = preprocess_query(query)

    # --- Math Layer ---
    if intent in ["calculate", "derivative", "integral"]:
        result = math_layer(intent, content)
        memory["last_query"] = query
        memory["last_result"] = result
        return f"Calculation result: {result}", None

    # --- CSV Layer ---
    if intent == "file_analysis":
        response, df = csv_analysis_layer(content)
        memory["last_query"] = query
        memory["last_result"] = response
        return response, df

    # --- Knowledge Layer ---
    knowledge_response = knowledge_layer(intent, content)
    if knowledge_response:
        memory["last_query"] = query
        memory["last_result"] = knowledge_response
        return knowledge_response, None

    # --- Semantic Layer ---
    if model is not None and intent == "definition":
        try:
            query_emb = model.encode([query])
            similarities = cosine_similarity(query_emb, kb_embeddings)[0]
            best_idx = similarities.argmax()
            if similarities[best_idx] > 0.6:
                topic = list(kb_entries.kb_entries.keys())[best_idx]
                response = kb_entries.kb_entries[topic]
                memory["last_query"] = query
                memory["last_result"] = response
                return response, None
        except:
            pass

    # --- Fallback Layer ---
    fallback_response = fallback_layer(query)
    memory["last_query"] = query
    memory["last_result"] = fallback_response
    return fallback_response, None
