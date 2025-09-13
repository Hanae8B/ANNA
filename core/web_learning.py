import requests
from bs4 import BeautifulSoup
import core.knowledge_base as kb
import time

knowledge_base = kb.KnowledgeBase()

def fetch_arxiv(query: str, max_results=5):
    base_url = "https://export.arxiv.org/api/query?search_query="
    query_url = f"{base_url}{query.replace(' ', '+')}&start=0&max_results={max_results}"
    try:
        response = requests.get(query_url, headers={"User-Agent": "ANNA-Agent"})
        if response.status_code != 200:
            return f"(arXiv Error {response.status_code})"
        soup = BeautifulSoup(response.text, "lxml-xml")
        entries = soup.find_all("entry")
        results = []
        for entry in entries:
            title = entry.title.text.strip()
            summary = entry.summary.text.strip()
            results.append(f"{title}\n{summary}\n")
            knowledge_base.store_query(query, f"{title}\n{summary}", tags=["arxiv"])
        time.sleep(3)  # respect API limits
        return "\n".join(results)
    except Exception as e:
        return f"(arXiv Exception: {str(e)})"

def fetch_pubmed(query: str, max_results=5):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    try:
        search_params = {'db': 'pubmed', 'term': query, 'retmode': 'json', 'retmax': max_results}
        r = requests.get(base_url, params=search_params)
        r.raise_for_status()
        ids = r.json().get("esearchresult", {}).get("idlist", [])
        results = []
        if ids:
            summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
            summary_params = {'db': 'pubmed', 'id': ",".join(ids), 'retmode': 'json'}
            s = requests.get(summary_url, params=summary_params)
            s.raise_for_status()
            summaries = s.json().get("result", {})
            for uid in ids:
                doc = summaries.get(uid, {})
                title = doc.get("title", "")
                source = doc.get("source", "")
                results.append(f"{title} ({source})")
                knowledge_base.store_query(query, f"{title} ({source})", tags=["pubmed"])
            time.sleep(1)  # respect rate limits
        return "\n".join(results) if results else "(PubMed: No results found)"
    except Exception as e:
        return f"(PubMed Exception: {str(e)})"

def fetch_wikipedia(query: str):
    from urllib.parse import quote
    base_url = "https://en.wikipedia.org/w/api.php"
    normalized_query = query.replace(" ", "_")
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
        "titles": normalized_query
    }
    r = requests.get(base_url, params=params, headers={"User-Agent": "ANNA-Agent"})
    r.raise_for_status()
    pages = r.json()["query"]["pages"]
    page_content = next(iter(pages.values())).get("extract", None)
    
    if page_content is None or len(page_content.strip()) == 0:
        # Fallback: Use search API
        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json"
        }
        r2 = requests.get(base_url, params=search_params, headers={"User-Agent": "ANNA-Agent"})
        r2.raise_for_status()
        search_results = r2.json()["query"]["search"]
        if search_results:
            first_title = search_results[0]["title"]
            return fetch_wikipedia(first_title)
        return "(Wikipedia: No content found)"
    return page_content

def autonomous_learn(query: str):
    kb_results = knowledge_base.retrieve_similar(query)
    if kb_results:
        combined = "\n\n".join([f"{r[0]}:\n{r[1]}" for r in kb_results])
        return f"(From KB)\n{combined}"

    sources = [fetch_arxiv(query), fetch_pubmed(query), fetch_wikipedia(query)]
    combined = "\n\n".join([s for s in sources if s])
    return combined if combined else "(ANNA: No information found from trusted sources)"
