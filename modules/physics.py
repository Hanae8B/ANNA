def analyze_quantum_query(query: str, data: str = None) -> str:
    q = query.lower()
    if "uncertainty" in q or "heisenberg" in q:
        canonical = ("The Heisenberg Uncertainty Principle states that there is a fundamental limit "
                     "to the accuracy with which we can measure both the position and momentum "
                     "of a particle simultaneously, arising from the wave nature of particles in quantum mechanics.")
        advice = ("Physics Analysis: Consider non-commuting operators, squeezed states, measurement disturbance, "
                  "and experimental setups for verification.")
        return f"{canonical}\n\n{advice}"

    if "epr" in q:
        canonical = ("The Einstein-Podolsky-Rosen paradox illustrates that quantum mechanics allows "
                     "entangled particles to have correlations that cannot be explained classically.")
        advice = ("Physics Analysis: Study Bell's theorem, violation of inequalities, and entanglement experiments.")
        return f"{canonical}\n\n{advice}"

    if "quantum gravity" in q or "unification" in q:
        canonical = ("Quantum gravity seeks a theory unifying general relativity and quantum mechanics, "
                     "explaining gravity at the Planck scale.")
        advice = ("Physics Analysis: Explore string theory, loop quantum gravity, asymptotic safety. "
                  "Consider Planck-scale phenomenology and cosmological implications.")
        return f"{canonical}\n\n{advice}"

    return "(Physics module: query not recognized. Try 'uncertainty', 'EPR', or 'quantum gravity')"
