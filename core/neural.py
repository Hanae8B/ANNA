import sympy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re

# Knowledge base entries
knowledge_base_entries = {
    "Heisenberg Uncertainty Principle": (
        "The Heisenberg Uncertainty Principle states that there is a fundamental limit "
        "to the accuracy with which the position and momentum of a particle can be measured simultaneously, "
        "arising from the wave nature of particles in quantum mechanics."
    ),
    "Hodge Conjecture": (
        "The Hodge Conjecture is an unsolved problem in algebraic geometry concerning the "
        "relationship between algebraic cycles and cohomology classes of a non-singular projective algebraic variety."
    ),
    "EPR Paradox": (
        "The Einstein-Podolsky-Rosen paradox highlights that quantum mechanics allows "
        "entangled particles to exhibit correlations that appear to violate local realism."
    ),
    "Double Slit Experiment": (
        "The double-slit experiment demonstrates that electrons and photons can behave both "
        "as particles and waves, creating interference patterns when not observed."
    ),
    "Quantum Gravity": (
        "Quantum gravity is the field of theoretical physics attempting to describe gravity "
        "according to the principles of quantum mechanics."
    ),
    "Unification of Theories": (
        "Unification of theories refers to the quest to combine the fundamental forces into a single framework."
    ),
    "Electron Stability": (
        "Electron stability refers to the observed fact that free electrons do not decay under normal conditions."
    ),
    "Fundamental Nature of Matter": (
        "The study of the fundamental nature of matter investigates elementary particles and their interactions."
    ),
    "Schrodinger Equation": (
        "The Schrodinger Equation governs the wavefunction evolution of quantum systems."
    ),
    "Quantum Entanglement": (
        "Quantum entanglement is a physical phenomenon where particles remain correlated "
        "even when separated by large distances."
    ),
    "General Relativity": (
        "General Relativity is Einstein's theory describing gravity as the curvature of spacetime."
    ),
    "Standard Model": (
        "The Standard Model describes the electromagnetic, weak, and strong nuclear interactions "
        "of elementary particles."
    ),
    # Add more advanced entries as needed
}

def normalize_text(text):
    return re.sub(r'[^a-z0-9 ]', '', text.lower())

def query_knowledge_base(query):
    norm_query = normalize_text(query)
    for topic, explanation in knowledge_base_entries.items():
        if normalize_text(topic) in norm_query or norm_query in normalize_text(topic):
            return explanation
    return None

def reason(query):
    """Return offline reasoning, calculations, or fallback."""
    # 1. Check knowledge base
    kb_result = query_knowledge_base(query)
    if kb_result:
        return kb_result

    # 2. Check for calculations
    if query.lower().startswith("calculate"):
        expr = query[len("calculate"):].strip()
        try:
            result = sympy.simplify(expr)
            return f"Calculation result: {result.evalf()}"
        except Exception as e:
            return f"Calculation error: {str(e)}"

    # 3. Fallback
    return (
        "ANNA: I could not find a direct offline explanation. "
        "Consider reviewing peer-reviewed scientific literature."
    )

def embed_query(query):
    """Dummy embedding for offline knowledge base"""
    return normalize_text(query)

def analyze_dataframe(df: pd.DataFrame):
    """Analyze uploaded CSV or data frame."""
    summary = df.describe(include='all')
    correlations = df.select_dtypes(include='number').corr()
    insights = []

    # Numeric insights
    numeric_cols = df.select_dtypes(include="number").columns
    for col in numeric_cols:
        std = df[col].std()
        mean = df[col].mean()
        insights.append(f"- {col} varies across samples (std={std:.3f}, mean={mean:.3f})")

    # Categorical insights
    cat_cols = df.select_dtypes(exclude="number").columns
    for col in cat_cols:
        top = df[col].mode()[0] if not df[col].mode().empty else "N/A"
        freq = df[col].value_counts().max() if not df[col].value_counts().empty else 0
        insights.append(f"- {col} most frequent value: {top} (freq={freq})")

    return summary, correlations, insights

def plot_dataframe(df: pd.DataFrame, output_dir="plots"):
    """Save histograms and correlation plot."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    numeric_cols = df.select_dtypes(include="number").columns
    hist_files = []
    for col in numeric_cols:
        plt.figure(figsize=(5,4))
        sns.histplot(df[col], kde=True, color='skyblue')
        plt.title(f"Histogram of {col}")
        fname = os.path.join(output_dir, f"{col}_hist.png")
        plt.savefig(fname)
        hist_files.append(fname)
        plt.close()

    # Correlation heatmap
    if len(numeric_cols) > 1:
        plt.figure(figsize=(6,5))
        sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm")
        corr_file = os.path.join(output_dir, "correlation.png")
        plt.savefig(corr_file)
        plt.close()
    else:
        corr_file = None

    return hist_files, corr_file
