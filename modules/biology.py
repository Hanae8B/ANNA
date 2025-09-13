def analyze_biology_query(query: str, data: str = None) -> str:
    q = query.lower()
    if "dna" in q or "gene" in q:
        canonical = "DNA stores genetic information in nucleotide sequences (A,T,C,G)."
        advice = "Transcription and translation decode DNA to proteins; consider CRISPR applications."
        return f"{canonical}\n\n{advice}"

    if "cell" in q or "mitochondria" in q:
        canonical = "Cells are the basic unit of life; mitochondria produce ATP via oxidative phosphorylation."
        advice = "Study organelle functions, energy metabolism, and bioengineering applications."
        return f"{canonical}\n\n{advice}"

    if "protein" in q or "enzyme" in q:
        canonical = "Proteins: amino acid chains; enzymes catalyze reactions."
        advice = "Analyze structure-function; enzyme kinetics; synthetic biology applications."
        return f"{canonical}\n\n{advice}"

    return "(Biology module: query not recognized. Try 'DNA', 'cell', or 'protein')"
