# Insurance Product Price Validation & Correction

This project implements validation and automatic correction of insurance product prices
according to a predefined set of business rules.

The solution is designed to:
- detect pricing inconsistencies
- report all detected violations
- automatically fix invalid prices in a deterministic and scalable way

---
## Requirements

- Python 3.12.3
- pip 25.3

---

## Running the Project

### Setup & Install dependencies (Windows)
```bash
python -m venv .venv

.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip

pip install -r requirements.txt
```

### Run main
```bash
python -m src.main
```
### Running Tests

```bash
python -m pytest -q
```

### Project Structure

```bash
src/
├── parsing.py
├── validation.py
├── fixing.py
├── models.py
├── ranks.py
├── utils.py
├── main.py
tests/
├── test_parsing.py
├── test_validation.py
├── test_fixing.py
```
---
## Pricing Rules

Prices must satisfy the following ordering constraints:

### Product hierarchy
MTPL < Limited Casco a< Casco



### Variant hierarchy (Limited Casco / Casco)
Compact / Basic < Comfort < Premium



### Deductible hierarchy (Limited Casco / Casco)
100 € < 200 € < 500 €
(higher deductible implies lower price)



---

## Design Principles

- Product, variant and deductible priorities are stored in dictionaries
- All comparisons are done using numeric ranks, not string comparisons
- Business logic operates on priorities to ensure scalability
- Fixing is performed **in-place** on the input price dictionary

---

## Core Components

### 1. `build_price_items`

**Purpose:**  
Parse the input price dictionary into structured objects.

**Description:**
- Iterates through the input dictionary
- Parses each key into product, variant and deductible
- Stores the parsed data in a `PriceElement` object
- Each `PriceElement` keeps the original key, enabling direct updates of the input dictionary

**Output:**  
A list of `PriceElement` objects.

---

### 2. `detect_inconsistencies`

**Purpose:**  
Detect and report all pricing rule violations.

**Description:**
- Works on the list of `PriceElement` objects
- Iterates over all pairs of products
- Applies all pricing rules independently:
  - product ordering
  - variant ordering
  - deductible ordering
- Collects all detected violations into a readable report

**Output:**  
- A multiline string describing all inconsistencies  
- An empty string if no violations are found

---

### 3. `fix_products_inplace`

**Purpose:**  
Automatically fix invalid prices.

The function iterates over all product pairs and applies corrective scaling
depending on the detected type of disorder.

#### Helper: `validate_or_fix_avg_prices`

- Validates average product prices provided as input
- Ensures:
  - all required products are present
  - all values are positive
  - higher-priority products have higher average prices
- If validation fails or no averages are provided, default values are used:
MTPL = 400
Limited Casco = 800
Casco = 1200



---

## Fixing Logic Overview

### Product disorder

Occurs when:
same variant and same deductible
but a lower-priority product is more expensive



**Fix strategy:**
factor = avg(higher_product) / avg(lower_product)
new_price = lower_price * factor



#### Possible cases
- **Lower product is MTPL (core product):**
  - Scale all higher-priority products
  - First compute the new minimum price
  - Then scale the entire product group

- **Lower product is Limited Casco:**
  - Only the corresponding Casco product is adjusted
  - No additional group scaling is required

---

### Deductible disorder

Occurs when:
same product and same variant
but higher deductible is more expensive



**Fix strategy:**
- deductible_100 = base
- deductible_200 = base * 0.9
- deductible_500 = base * 0.9 * 0.9



The entire product–variant group is scaled accordingly.

---

### Variant disorder

Occurs when:
same product and same deductible
but a lower-priority variant is more expensive



**Fix strategy:**
- Use the highest-priority variant price as base
- Increase each subsequent variant by 7% ( same way as variant disorder )

---




