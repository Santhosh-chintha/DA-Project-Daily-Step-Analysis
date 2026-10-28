# 👟 Daily Step Analysis Dashboard

A beginner-friendly daily step-count analysis and visualization dashboard built with **Python**, **Pandas**, **Matplotlib**, and **Streamlit**.

This application analyzes walking activity from a CSV file, calculates core health metrics against a customizable daily step goal, visualizes trends using clear charts, and displays structured daily activity records.

---

## 📌 Project Overview

* **Instant Out-of-the-Box Execution**: Comes pre-packaged with `steps.csv` containing 35 days of sample activity data so you can run it immediately.
* **Custom CSV Upload**: Easily upload your own step records to dynamically update all statistics and visualizations.
* **Interactive Goal Adjustment**: Adjust your daily step goal via the sidebar (defaults to 8,000 steps).
* **Robust Error Handling**: Automatically handles missing dates, invalid non-numeric values, and corrupt entries gracefully with helpful user messages.

> **Note on Sample Data:** The included `steps.csv` file contains synthetically generated sample data created solely for demonstration and educational purposes. It does not represent personal or medical measurements from an actual individual.

---

## 🚀 Features

1. **Top-Level KPI Cards**:
   - **Total Steps**: Total cumulative steps taken across the dataset.
   - **Average Daily Steps**: Daily average compared against your chosen goal.
   - **Highest Step Count**: Peak step count and the exact date it was achieved.
   - **Lowest Step Count**: Minimum step count and the corresponding date.
   - **Goal Achieved Days**: Number of days meeting or exceeding the goal with percentage success rate.

2. **Visualizations**:
   - **Line Chart**: Daily steps over time with a reference goal line.
   - **Bar Chart**: Direct comparison of daily step counts with overall average.
   - **Goal Comparison Bar Chart**: Color-coded visualization (Green for goal achieved, Red for goal missed) with a target threshold line.

3. **Data Records Table**:
   - Complete table showing Date, Step Count, Goal Status (`✅ Goal Met` / `❌ Missed`), and Goal Difference.
   - One-click CSV export of the cleaned activity records.

4. **Data Upload & Validation**:
   - Sidebar file uploader for custom CSV files.
   - Validates required columns (`Date` and `Steps`), converts dates and numeric values, filters invalid records, and sorts chronologically.

---

## 🛠️ Technologies Used

* **Python 3.8+**
* **[Pandas](https://pandas.pydata.org/)** for data loading, cleaning, and statistical calculations.
* **[Matplotlib](https://matplotlib.org/)** for plotting line charts and bar charts.
* **[Streamlit](https://streamlit.io/)** for the web application dashboard interface.

---

## 📁 Project Structure

```text
daily-step-analysis/
│
├── app.py              # Main Streamlit application and visualization logic
├── steps.csv           # 35-day realistic sample dataset
├── requirements.txt    # Python library dependencies
└── README.md           # Documentation and setup instructions
```

---

## ⚙️ Installation & Setup Instructions

Follow these simple steps to run the dashboard locally on your machine:

### 1. Prerequisites
Ensure you have **Python 3.8 or higher** installed on your system. You can check your version in a terminal:
```bash
python --version
```

### 2. Navigate to the Project Directory
Open your terminal or PowerShell and move into the `daily-step-analysis` folder:
```bash
cd path/to/daily-step-analysis
```

### 3. (Recommended) Create and Activate a Virtual Environment

- **On Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **On macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 4. Install Dependencies
Install all required libraries using `pip`:
```bash
pip install -r requirements.txt
```

### 5. Launch the Dashboard
Run the Streamlit application:
```bash
streamlit run app.py
```

Your default web browser will automatically open the dashboard at:
```
http://localhost:8501
```

---

## 📊 CSV File Format Requirements

If you wish to upload your own CSV file, ensure it has the following format:

| Column Name | Required | Description | Example |
| :--- | :--- | :--- | :--- |
| `Date` | **Yes** | Date of activity (YYYY-MM-DD or standard date format) | `2024-10-01` |
| `Steps` | **Yes** | Total steps taken on that day (positive integer) | `8450` |
| `Calories_Burned` | No | Estimated calories burned during the day | `2310` |

### Sample CSV snippet:
```csv
Date,Steps,Calories_Burned
2024-10-01,7450,2150
2024-10-02,8200,2280
2024-10-03,9120,2410
```

---

## 💡 How to Use the Dashboard

1. **Explore the Sample Dataset**: The dashboard starts up loaded with `steps.csv` automatically.
2. **Adjust Your Goal**: Use the **Daily Step Goal** input in the sidebar to change the target (default: 8,000 steps). Observe how KPI cards and charts update immediately.
3. **Switch Between Chart Tabs**:
   - Click **📈 Daily Steps Over Time** to examine trends.
   - Click **📊 Step Counts Comparison** to view day-to-day fluctuations.
   - Click **🎯 Steps vs. Daily Goal** to quickly spot which days hit target.
4. **Upload Your Custom Data**: Drag-and-drop or browse for your own CSV file in the sidebar.
5. **Download Cleaned Data**: Use the download buttons to save the sample template or export cleaned activity tables.
