# Trade Reconciliation Analysis - Naveed Ul Mustafa

## Overview
Trade reconciliation between internal power trading records and clearer settlement data.

## Objective
Reconcile monthly delivery positions by decomposing quarterly contracts and netting overlapping positions.

## Data Structure
- **Internal Data**: Monthly outright trades + Q2 2025 quarterly contract
- **Clearer Data**: Monthly settlement breakdown

## Key Features
- Quarterly contract decomposition (cascading)
- Position netting for overlapping months
- Price-weighted averaging
- Comprehensive reconciliation analysis

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip
- Jupyter Notebook

### Installation

1. Clone the repository:
```bash
git clone https://github.com/numustafa/numustafa_trade_reconciliation.git
cd numustafa_trade_reconciliation
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt

```

## Usage

```bash
jupyter notebook notebooks/numustafa_trade_reconciliation.ipynb
```

### Run All Tests
```bash
python -m pytest tests\test_stress.py -v -s
python -c "from utils.stress import *; print(f"stress.py imported successfully")"
python -c "from utils.reconciliation import *; print(f"reconciliation.py imported successfully")"
python -c "from utils.data_loader import *; print(f"data_loader.py imported successfully")"
python -c "from utils.data_loader import * try : inteernl = load_data('data/internal_data.xlsx'); clearer = load_data('data/clearer_data.xlsx'); print(f"Internal Data : {len(inteernl)} records, Clearer Data: {len(clearer)} records") except Exception as e: print(f"Error loading data: {e}")"

```


## Results
[Brief summary of findings]


### Running the Analysis

## Quick Start with GitHub Codespaces

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/numustafa/numustafa_trade_reconciliation)

## Contact
Naveed Ul Mustafa - [mustafa@c.tu-berlin.de](mailto:mustafa@campus.tu-berlin.de) - [LinkedIn](https://www.linkedin.com/in/numustafa)

