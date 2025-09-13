def solve_math_query(query: str, data: str = None) -> str:
    q = query.lower()
    if "quadratic" in q:
        canonical = "Quadratic equations: ax^2 + bx + c = 0. Solutions: x = [-b ± sqrt(b^2 - 4ac)] / 2a."
        advice = "Math Analysis: Check discriminant; consider real vs complex solutions."
        return f"{canonical}\n\n{advice}"

    if "derivative" in q or "integral" in q:
        canonical = "Derivative: rate of change. Integral: area under curve."
        advice = "Math Analysis: Use chain/product rules; integration by parts. Apply to physics or engineering."
        return f"{canonical}\n\n{advice}"

    if "matrix" in q or "eigenvalue" in q:
        canonical = "Matrix: linear transformations. Eigenvalues/vectors satisfy A*v = λ*v."
        advice = "Math Analysis: Compute determinant and characteristic polynomial; apply in physics or data analysis."
        return f"{canonical}\n\n{advice}"

    return "(Mathematics module: query not recognized. Try 'quadratic', 'derivative', or 'matrix')"
