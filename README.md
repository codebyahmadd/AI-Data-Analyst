# 🤖 AI Data Analyst

An intelligent and interactive data analysis application built with **Python and Streamlit** that helps users explore, clean, visualize, and understand their datasets with minimal effort.

The application allows users to upload a CSV file and provides automated data analysis, visualizations, sales forecasting, AI-powered insights, report generation, and a conversational interface for asking questions about the data.

---

## 🚀 Features

### 📂 1. Upload CSV
- Upload your own CSV dataset.
- Automatically loads and prepares the dataset for analysis.
- Supports different datasets without requiring manual code changes.

### 📊 2. Data Overview
- View dataset dimensions and basic information.
- Explore columns, data types, and sample records.
- Get a quick understanding of the uploaded dataset.

### 🧹 3. Data Cleaning
- Detect missing values.
- Handle duplicate records.
- Identify data quality issues.
- Automatically prepare data for further analysis.

### 📈 4. Advanced Visualization
- Generate interactive charts from the dataset.
- Explore relationships between different variables.
- Visualize categorical and numerical data.
- Use charts to discover patterns and trends.

### 📅 5. Sales Trend Analysis
- Analyze sales performance over time.
- Identify upward and downward trends.
- Explore changes in revenue and sales activity.

### 🔮 6. Sales Forecasting
- Generate sales forecasts from historical data.
- Visualize expected future sales.
- Use historical trends to support better decision-making.

### 🧠 7. AI Insights & KPIs
- Automatically generate meaningful insights from the dataset.
- Identify important business metrics.
- Highlight key performance indicators.
- Discover trends and notable changes in the data.

### 📄 8. Reports
- Generate analytical reports from the uploaded dataset.
- Present important findings in an organized format.
- Make data analysis easier to share and understand.

### 💬 9. Chat with Data
- Ask questions about your dataset in natural language.
- Get answers based on the uploaded data.
- Explore your dataset through an interactive conversational interface.

---

## 🛠️ Technologies Used

- **Python**
- **Pandas**
- **NumPy**
- **Plotly**
- **Streamlit**
- **OpenPyXL**
- **Python-dotenv**

---

## 📁 Project Structure

```text
AI-Data-Analyst/
│
├── assets/
│
├── data/
│
├── models/
│
├── notebooks/
│
├── pages/
│   ├── chat.py
│   ├── insights.py
│   ├── overview.py
│   ├── reports.py
│   └── visualization.py
│
├── reports/
│   ├── pdf_report.py
│   └── report_generator.py
│
├── utils/
│   ├── components/
│   │   ├── header.py
│   │   └── sidebar.py
│   │
│   ├── ai_chat.py
│   ├── ai_insights.py
│   ├── chart_generator.py
│   ├── data_cleaner.py
│   ├── data_loader.py
│   ├── data_summary.py
│   ├── health_score.py
│   └── statistics.py
│
├── app.py
├── requirements.txt
└── README.md