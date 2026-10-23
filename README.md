# Retail Inventory Demand Forecasting and Stock-Out Prediction

## Project Overview

Retail businesses often face challenges in maintaining optimal inventory levels. Overstocking increases storage costs, while understocking can lead to lost sales and dissatisfied customers.

This project uses **Machine Learning and Data Analytics** to forecast product demand and identify potential stock-out risks. It analyzes historical retail data to help businesses make better inventory management and replenishment decisions.

The project was developed as part of a college field project for the **B.Sc. Data Science** program.

## Objectives

- Analyze historical retail sales and inventory data.
- Forecast product demand using machine learning.
- Identify potential stock-out situations.
- Compare the performance of different forecasting models.
- Analyze factors affecting product demand.
- Support inventory planning through data-driven insights.

## Technologies Used

- **Programming Language:** Python
- **Data Analysis:** Pandas, NumPy
- **Data Visualization:** Matplotlib, Seaborn
- **Machine Learning:** Scikit-learn
- **Dashboard:** Streamlit
- **Development Environment:** Jupyter Notebook / Python IDE

## Dataset Description

The dataset contains approximately **76,000 records** of retail sales and inventory information covering January 2022 to January 2024.

Key attributes include:

- Date
- Store and product information
- Product category
- Region
- Units sold
- Inventory levels
- Promotional activity
- Epidemic-related conditions
- Demand-related information

The dataset was used to explore sales patterns, identify demand drivers, and develop forecasting and stock-out prediction models.

## Methodology

### 1. Data Preprocessing
- Inspected the dataset and checked for missing values.
- Examined data types and feature distributions.
- Prepared relevant features for machine learning.
- Used a chronological train-test split to evaluate demand forecasting.

### 2. Exploratory Data Analysis (EDA)
- Analyzed demand across stores, products, and categories.
- Examined the impact of promotions and external conditions.
- Identified trends and patterns in retail demand.
- Investigated inventory shortages and zero-inventory records.

### 3. Demand Forecasting

Two regression models were evaluated:

- **Random Forest Regressor:** Predicts demand using multiple decision trees and combines their predictions.
- **Gradient Boosting Regressor:** Builds sequential decision trees to improve predictions by learning from previous errors.

### 4. Stock-Out Prediction

A Random Forest Classifier was used to classify potential stock-out cases based on the available data.

The stock-out classification task presented a significant challenge because actual stock-out cases represented only a small proportion of the dataset.

### 5. Inventory Analysis

The project explores inventory management concepts such as reorder points, safety stock, and replenishment planning to support better inventory decisions.

## Model Performance

### Demand Forecasting Results

| Metric | Random Forest | Gradient Boosting |
|---|---:|---:|
| R² Score | 0.8721 | 0.8634 |
| MAE | 12.0929 | — |
| RMSE | 15.7673 | — |

Random Forest achieved an R² score of approximately **0.87**, indicating a strong fit on the evaluated test dataset. The MAE and RMSE quantify the prediction errors in the demand target's units.

### Stock-Out Classification Results

The Random Forest Classifier achieved an accuracy of approximately **99.51%**. However, it failed to identify positive stock-out cases in the reported experiment, resulting in zero precision, recall, and F1-score for the positive class.

This highlights the limitations of accuracy when working with highly imbalanced datasets. Further work is needed to improve stock-out detection using techniques such as class weighting, resampling, threshold tuning, and precision-recall evaluation.

## Key Findings

- Random Forest performed better than Gradient Boosting on the evaluated demand forecasting metrics.
- Promotional activity was associated with higher average demand in the analyzed dataset.
- Demand varied across products, stores, and external conditions.
- Stock-out cases were rare compared with non-stock-out cases.
- Accuracy alone was insufficient to evaluate the stock-out classification model.

## Project Features

- Retail sales and inventory analysis
- Demand forecasting using machine learning
- Comparison of regression models
- Stock-out classification
- Data visualization and exploratory analysis
- Inventory planning and replenishment insights
- Streamlit-based interactive dashboard

## How to Run the Project

### Prerequisites

Install Python and the required libraries.

### 1. Clone the repository

```bash
git clone <https://github.com/yajat-17/retail-inventory-demand-forecasting>
```

### 2. Open the project folder

```bash
cd <YOUR_PROJECT_FOLDER>
```

### 3. Install dependencies

If a `requirements.txt` file is available:

```bash
pip install -r requirements.txt
```

Otherwise, install the main libraries:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn streamlit
```

### 4. Run the application

If the Streamlit application is named `app.py`:

```bash
streamlit run app.py
```

The dashboard will open in your browser.

*Note: Update these instructions to match the actual filenames and folder structure in your repository.*

## Future Improvements

- Improve stock-out detection using imbalanced-learning techniques.
- Evaluate classification models using precision, recall, F1-score, and PR-AUC.
- Incorporate additional demand drivers and external data.
- Improve forecasting at the individual product and store level.
- Add real-time inventory alerts and replenishment recommendations.
- Deploy the dashboard for wider accessibility.

## Conclusion

This project demonstrates how machine learning can be applied to retail demand forecasting and inventory analysis. The forecasting experiments produced promising results, while the stock-out classification experiment revealed the challenges of detecting rare events. The findings provide a foundation for developing more reliable, data-driven inventory management solutions.

## Author

**Yajat Eppakayala**

B.Sc. Data Science  
SIES College of Arts, Science and Commerce, Sion, Mumbai

---

*Academic Field Project | Machine Learning | Retail Analytics | Inventory Management*
