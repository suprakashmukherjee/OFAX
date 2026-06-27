# OFAX

> **Scale your sanctions screening validation.**  
> *Automated test data generation for modern compliance teams.*

---

## Overview

**OFAX (OFAC Xplorer)** is a Python-based automation framework that simplifies the creation of **sanctions screening test datasets** by automating searches against the **U.S. Department of the Treasury's OFAC Sanctions Search** portal.

Given a list of known entity names and a configurable minimum name match score, OFAX performs automated searches, collects the returned search results, and consolidates them into a structured dataset suitable for testing and validating sanctions screening systems.

The objective is to eliminate repetitive manual searches and enable compliance, QA, and engineering teams to generate large-scale validation datasets in minutes.

---

## Why OFAX?

Sanctions screening systems are only as good as the datasets used to validate them.

Compliance teams often need hundreds or thousands of realistic test cases to evaluate:

- Name matching algorithms
- Fuzzy matching behavior
- Screening engine performance
- Regression testing after model or rule changes
- False positive analysis (out of scope of this project)

Performing these searches manually through the OFAC search portal is time-consuming and difficult to scale.

**OFAX automates the entire workflow.**

---

## Features

- 🚀 Automated OFAC sanctions search
- 🔍 Configurable minimum name match score
- 📋 Batch processing of multiple search keywords
- 🤖 Selenium-powered browser automation
- 🖥️ Headless browser support
- 📥 Automatic extraction of search results
- 📊 Consolidated dataset generation
- 📁 CSV export for downstream validation and testing
- ⚡ Designed for large-scale screening dataset generation

---

## Workflow

```text
Input Entity Names
        │
        ▼
Launch Headless Browser
        │
        ▼
Open OFAC Search Portal
        │
        ▼
Enter Search Keyword
        │
        ▼
Set Minimum Match Score
        │
        ▼
Execute Search
        │
        ▼
Extract Search Results
        │
        ▼
Repeat for All Input Names
        │
        ▼
Merge Results
        │
        ▼
Generate Screening Test Dataset
```

---

## Input

Provide a list of entity names to search.

Example:

```text
OSAMA BIN LADEN
VLADIMIR PUTIN
AL QAIDA
BANK MELLI
JOHN SMITH
```

Specify the minimum OFAC name match score.

Example:

```text
Minimum Name Score: 90
```

---

## Output

OFAX consolidates all returned search results into a single dataset.

| Search Term | Name | Address | Type | Programs | List | Score |
|-------------|------|----------|------|-----------|------|------:|
| OSAMA BIN LADEN | USAMA BIN LADEN | Afghanistan | Individual | SDGT | SDN | 100 |
| OSAMA BIN LADEN | OSAMA BIN LADIN | Pakistan | Individual | SDGT | SDN | 98 |
| VLADIMIR PUTIN | VLADIMIR PUTIN | Russia | Individual | RUSSIA | SDN | 100 |

Each row represents a sanctioned record returned by the OFAC search engine for the corresponding search keyword.

---

## Use Cases

### Compliance Engineering

Generate realistic datasets to validate sanctions screening systems.

### Quality Assurance

Stress test sanctions screening engines using authentic OFAC search results.

### Regression Testing

Validate screening engine behavior after updates to matching algorithms or business rules.

### Model Validation

Evaluate fuzzy matching performance across a large number of sanctioned entities.

### Internal Compliance Tooling

Automate repetitive search and dataset generation tasks for compliance and engineering teams.

---

## Technology Stack

- Python
- Selenium
- Chrome WebDriver
- Pandas
- CSV Export

---

## Project Structure

```text
OFAX/
│
├── input/
│   └── entity_names.csv
│
├── output/
│   ├── search_results.csv
│   └── logs/
│
├── src/
│   ├── search_entities.py
│   ├── process_data.py
│   └── exporter.py
│
├── requirements.txt
└── README.md
```

---

## Example Workflow

1. Read the input list of entity names.
2. Launch a headless browser.
3. Navigate to the OFAC Search Portal.
4. Configure the minimum name match score.
5. Execute the search.
6. Capture all returned search results.
7. Repeat for every search keyword.
8. Merge all results into a single dataset.
9. Export the final dataset as CSV.

---

## Who Is This For?

- Compliance Engineers
- AML & Sanctions Teams
- Payments Technology Companies
- Banking Technology Teams
- QA Engineers
- Risk Analytics Teams
- Financial Crime Technology Teams

---

## Disclaimer

OFAX is intended to automate the generation of **sanctions screening validation datasets** using publicly available search results. It is designed to support testing, quality assurance, and compliance engineering workflows.

Users are responsible for ensuring that their use of the OFAC search portal complies with applicable website terms, policies, and legal requirements. OFAX is **not affiliated with, endorsed by, or sponsored by** the U.S. Department of the Treasury or the Office of Foreign Assets Control (OFAC).

---

## Roadmap

- Support additional sanctions sources (EU, UK, UN, etc.)
- Parallel search execution
- Configurable retry and rate limiting
- Audit logging
- Docker support
- REST API
- Interactive dashboard
- CI/CD integration
- Test dataset versioning

---

## License

MIT License

---

# OFAX

**Scale your sanctions screening validation.**

*Automated test data generation for modern compliance teams.*
