# ANNA - Autonomous Neural Navigator & Advisor

**ANNA** is a fully offline, multi-disciplinary scientific AI assistant designed to provide reasoning, calculations, and data analysis for advanced scientific topics. It integrates symbolic computation, numeric analysis, and interactive visualization in a smart GUI interface.

---

## Features

- **Offline Scientific Reasoning**
  - Answers advanced queries in physics, chemistry, mathematics, biology, and engineering.
  - Supports multi-disciplinary reasoning using a local knowledge base.

- **Calculations**
  - Symbolic math using `SymPy` (integrals, derivatives, equations).
  - Numeric calculations using `NumPy`.

- **Data Analysis**
  - Upload and analyze CSV datasets.
  - Computes statistics, correlations, and generates insights.
  - Inline plotting with `Matplotlib` and `Seaborn`.

- **Interactive GUI**
  - Submit queries via **Enter key** or **button click**.
  - Inline results display, including calculation and data analysis outputs.
  - Customizable background images.
  - Ethical action controls (confirms before executing critical actions).

- **Expandable Knowledge Base**
  - Add new topics offline with punctuation-stripped and fuzzy matching for reliable answers.
  - Stores knowledge in `core/kb_entries.py`.

---

## Requirements

- Python 3.10+
- Required packages:
  ```bash
  pip install numpy pandas sympy matplotlib seaborn tk

(Optional for drag-and-drop file support)
pip install tkinterdnd2

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

Populate Knowledge Base

python populate_knowledge_base.py


This populates ANNA with scientific knowledge and embeddings.

Run ANNA GUI

python main.py


Type scientific queries or calculations in the input box.

Press Enter or click Analyze Query.

For CSV data analysis, drag and drop the file or specify its path.

Example Queries

calculate 2+2

integrate x**2 dx

Heisenberg Uncertainty Principle

Hodge Conjecture

analyze file C:/ANNA/data/sample_data.csv

Notes

ANNA currently works offline and relies on its local knowledge base.

Web scraping or external database access can be added in neural.py while respecting site Terms of Service.

The GUI background can be customized by replacing background.png.

License

This project is for educational and research purposes. Use responsibly and ethically. Redistribution or commercial use requires permission.

Authors

Designed and developed by Anna Baniakina

Inspired by AI-driven scientific assistants and expert research advisory systems.