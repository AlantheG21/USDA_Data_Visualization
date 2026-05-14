# USDA Food Nutrition Profiling

**CS 4379G — Data Analysis and Visualization | Texas State University | Spring 2026**
**Alan Garcia**

---

## Overview

This project explores nutritional patterns across 7,793 foods from the USDA Standard Reference (SR Legacy) dataset. Using seven core nutrients — protein, fat, carbohydrates, sugar, fiber, sodium, and calories — the analysis identifies how foods naturally cluster into distinct nutritional archetypes and what those groups reveal about the difference between whole foods and ultra-processed ones.

**Key findings:**
- Fat is the primary driver of caloric density across all food categories.
- Sodium is the clearest measurable marker of ultra-processed foods.
- K-means clustering (k=7) reveals nutritional archetypes that cut across USDA category labels — foods from different grocery sections often share more in common nutritionally than their labels suggest.

The seven clusters identified are: Low-Calorie Whole Foods, Animal Proteins, Calorie-Dense Fats & Oils, Extreme Sodium Outliers, High-Fiber Legumes & Seeds, Processed Grains & Breads, and Sweets & Sugary Foods.

For a more detailed rundown over the project, read over the narrative under the `narrative/` folder

**Data source:** [USDA FoodData Central — SR Legacy Dataset (2019)](https://fdc.nal.usda.gov/download-datasets)

---

## Project Structure

```
FinalProject/
├── data/                         # Raw and processed CSV files
│   ├── food.csv
│   ├── food_category.csv
│   ├── food_nutrient.csv
│   ├── nutrient.csv
│   ├── food_nutrients_clean.csv  # Cleaned wide-format dataset
│   └── food_nutrients_clustered.csv  # With cluster labels
├── notebooks/
│   └── usdaFoodNutrition.ipynb   # Full analysis (EDA + clustering)
├── dashboard/
│   └── app.py                    # Streamlit dashboard
├── narrative/
│   └── narrative.md              # Written project narrative
├── assets/                       # Exported visualization images
└── requirements.txt
```

---

## Requirements

- Python 3.12+
- Dependencies listed in `requirements.txt`:
  - streamlit, pandas, numpy, plotly, scikit-learn, matplotlib, seaborn

---

## Setup and Installation

### Using uv (recommended)

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create a virtual environment and install dependencies
uv venv
uv pip install -r requirements.txt
```

### Using venv (standard library)

```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

### Using conda

```bash
conda create -n usda-nutrition python=3.12
conda activate usda-nutrition
pip install -r requirements.txt
```

---

## Running the Project

### Jupyter Notebook

The notebook (`notebooks/usdaFoodNutrition.ipynb`) covers data cleaning, EDA, and k-means clustering. Run all cells top-to-bottom.

**With uv:**
```bash
source .venv/bin/activate
jupyter notebook notebooks/usdaFoodNutrition.ipynb
```

**With venv or conda** (after activating your environment):
```bash
jupyter notebook notebooks/usdaFoodNutrition.ipynb
```

> The notebook expects the raw data files to be present in `data/`. It will generate `food_nutrients_clean.csv` and `food_nutrients_clustered.csv` when run end-to-end.

---

### Streamlit Dashboard

The dashboard (`dashboard/app.py`) provides three interactive tabs:
- **Food Explorer** — search and filter individual foods by category and nutrient values
- **Cluster Explorer** — visualize the PCA projection and radar profiles for each nutritional cluster
- **Nutrient Comparison** — compare nutrient distributions across food categories

**With uv:**
```bash
source .venv/bin/activate
streamlit run dashboard/app.py
```

**With venv or conda** (after activating your environment):
```bash
streamlit run dashboard/app.py
```

The app will open at `http://localhost:8501` in your browser. It reads from `data/food_nutrients_clustered.csv`, so run the notebook first if that file is not present.
