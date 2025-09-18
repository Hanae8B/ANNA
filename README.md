# ANNA - Autonomous Neural Navigator & Advisor

**ANNA** is a fully offline, multi-disciplinary scientific AI assistant. It provides reasoning, calculations, and data analysis for scientific topics using symbolic computation, numeric analysis, and an interactive GUI.

---

## Features

### Offline Scientific Reasoning
- Answers queries in **physics, chemistry, mathematics, biology, and engineering**.
- Can respond to casual language queries, e.g., `"hello, can you calculate 2+2"`.
- Provides **definitions and explanations** from a local knowledge base.
- Generates **comparative answers**, e.g., `"difference between bacteria and virus"`:
Bacteria vs Virus:

bacteria: Single-celled microorganisms that can be beneficial or pathogenic. Applications: medicine, biotechnology, microbiology.

virus: Non-living infectious agents that require host cells to replicate. Applications: medicine, virology, epidemiology.
Differences: Bacteria and Virus have distinct properties.

### Calculations
- **Basic arithmetic**: addition, subtraction, multiplication, division.
- **Symbolic math** using `SymPy`:
- Integrals, derivatives
- Basic symbolic evaluation
- Automatic rounding of numeric results for clean output:
Query: calculate 2+2
ANNA Response: Calculation result: 4.0

Query: integrate x**2 dx
ANNA Response: Calculation result: 2.0

Query: derivative of sin(x)
ANNA Response: Calculation result: cos(x)

### Scientific Knowledge
- Supports queries in **quantum mechanics, molecular biology, mathematics**, etc.
- If a topic is not in the knowledge base, provides a fallback message to consult peer-reviewed literature:

Query: Hodge Conjecture
ANNA Response: ANNA could not find a direct offline explanation. Please consult peer-reviewed scientific literature.

### Data Analysis
- Upload and analyze **CSV datasets**.
- Computes:
- **Numeric correlations** between columns (e.g., Pearson correlation).
- **Categorical counts** and most common values.
- Provides **insights based on correlations**:

Query: analyze file C:/ANNA/data/sample_data.csv
ANNA Response:
Data Summary: 50 rows, 6 columns.
Numeric columns: ExperimentID, Temperature, Pressure, Voltage, Current
Strong correlations:
Temperature ↔ Pressure = 0.92
Temperature ↔ Voltage = 0.98
Temperature ↔ Current = 0.98
Pressure ↔ Voltage = 0.92
Pressure ↔ Current = 0.92
Voltage ↔ Current = 0.97
Categorical column counts:

Material: most common = Aluminum, counts = {'Aluminum': 25, 'Copper': 25}

(Insight) Temperature ↔ Current correlation = 0.98

### Interactive GUI
- **Full background support** (`background.png`) for a futuristic look.
- Input and output boxes: **white background, black letters**.
- **Buttons:** dark blue with white text.
- Submit queries via **Enter key** or **button click**.
- Displays **calculations, knowledge responses, and CSV analysis results**.

---

## Requirements

- Python 3.10+
- Packages:
```bash
pip install numpy pandas sympy matplotlib seaborn tk pillow fuzzywuzzy scikit-learn feedparser requests

Optional AI/semantic features:

pip install sentence-transformers torch
File Structure
C:\ANNA
│   main.py
│   populate_knowledge_base.py
│   background.png
│
└───core
    │   neural.py
    │   navigator.py
    │   knowledge_base.py
    │   kb_entries.py
Setup Instructions
1. Populate Knowledge Base
python populate_knowledge_base.py


This populates ANNA with scientific knowledge.

2. Run ANNA GUI
python main.py


Type queries or calculations in the input box.

Press Enter or click Analyze Query.

For CSV analysis, specify the file path.

Example Queries
calculate 2+2
integrate x**2 dx
derivative of sin(x)
Heisenberg Uncertainty Principle
Hodge Conjecture
difference between bacteria and virus
analyze file C:/ANNA/data/sample_data.csv

Notes

ANNA works offline using its local knowledge base.

Provides fuzzy matching and comparative answers.

GUI customization possible via background.png and button styles.

Current GUI shows white boxes with black letters and dark blue buttons.
![ANNA GUI](assets/images/anna_gui.png)

License

Educational and research purposes only. Use responsibly.

Authors

Developed by Anna Baniakina.
Inspired by AI-driven scientific assistants and expert research advisory systems.