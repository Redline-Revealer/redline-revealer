# CONTRIBUTING GUIDELINES FOR REDLINE REVEALER

Thank you for considering contributing to Redline Revealer! This project aims to help visualize the legacy of redlining and promote housing equity through responsible AI.

---

## 🧠 Project Overview
Redline Revealer is a civic tech platform powered by Streamlit, Azure AI, and Power BI. It features:
- 🧭 Historical redlining map overlays
- 🤖 LLM-powered legal assistant for heirs property guidance
- 📊 Risk scoring engine for housing instability
- 📈 Policy dashboards using Power BI

---

## ✅ Getting Started
1. **Fork the Repository**
2. **Clone Your Fork**
   ```bash
   git clone https://github.com/your-username/redline-revealer.git
   cd redline-revealer
   ```
3. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make Changes & Commit**
5. **Push to Your Branch**
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Open a Pull Request**

---

## 🔧 Development Guidelines
- Follow the naming convention: `feature/*`, `bugfix/*`, `hotfix/*`
- Write clear commit messages (e.g. `feat: add LLM assistant routing`)
- Keep PRs focused and under 500 lines if possible
- Tag issues in your PR using `Fixes #issue-number`

---

## 📂 Folder Structure

To keep the repo clean and organized, follow this structure when adding files:

```
redline-revealer/
├── assets/                    # App images, icons, logos, etc.
├── data/                      # All datasets
│   ├── housing/               # Housing data (Excel, CSVs, etc.)
│   └── maps/                  # GIS/GeoJSON/map files
├── docs/                      # General documentation
│   ├── roles/                 # Individual team role documentation
│   └── housing-risk-analysis.md  # Deep dives or explanatory writeups
├── src/                       # Source code for the Streamlit app
├── .github/workflows/         # CI/CD workflows
├── requirements.txt           # Dependencies
├── README.md                  # Project overview
├── CONTRIBUTING.md            # This file
└── LICENSE                    # MIT License
```

📌 **Note**: Do not create new README files. All high-level information belongs in `README.md`. Additional insights can be added to `/docs/`.

---

## 🧪 Running Tests
> _CI workflows will auto-run tests on pull requests (setup in `.github/workflows/ci.yml`)._

If you want to test locally:
```bash
python -m unittest discover tests
```

---

## 🚦 GitHub Actions CI (Pre-Configured)
Redline Revealer runs a basic CI check to validate:
- Python syntax errors (via `flake8`)
- Presence of tests
- Required `requirements.txt` lock compliance

A basic CI config lives in `.github/workflows/ci.yml`:
```yaml
name: Python Lint & Test

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install flake8

    - name: Lint code
      run: flake8 .

    - name: Run tests
      run: python -m unittest discover tests
```

---

## 🛡️ Code of Conduct
We believe in inclusivity and psychological safety. Please review our [Code of Conduct](CODE_OF_CONDUCT.md).

---

## 🙋 Need Help?
- Tag @portiajefferson in GitHub issues or use the project board for updates
- Drop feedback directly in the GitHub Discussions (if enabled)

---

Thanks for helping us build something meaningful!  
– The Redline Revealer Team

