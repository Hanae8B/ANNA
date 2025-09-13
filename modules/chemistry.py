def analyze_chemistry_query(query: str, data: str = None) -> str:
    q = query.lower()
    if "stoichiometry" in q or "reaction" in q:
        canonical = "Stoichiometry calculates quantitative relationships of reactants and products."
        advice = "Balance equations, compute mole ratios, consider limiting reagents and yields."
        return f"{canonical}\n\n{advice}"

    if "enthalpy" in q or "gibbs" in q:
        canonical = "Thermodynamics studies energy and entropy; Gibbs free energy predicts spontaneity."
        advice = "Use ΔG = ΔH - TΔS; apply to reactions, phase changes, and reaction optimization."
        return f"{canonical}\n\n{advice}"

    if "hysteresis" in q:
        canonical = "Hysteresis: lag between input and output in magnetic or mechanical systems."
        advice = "Area of loop measures energy dissipation; analyze magnetization curves."
        return f"{canonical}\n\n{advice}"

    return "(Chemistry module: query not recognized. Try 'reaction', 'enthalpy', or 'hysteresis')"
