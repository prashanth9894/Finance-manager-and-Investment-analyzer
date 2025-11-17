# 💰 Finance Manager & Investment Analyzer

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0%2B-0C4B33?logo=django)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3%2B-purple?logo=bootstrap)](https://getbootstrap.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub repo](https://img.shields.io/badge/GitHub-prashanth9894%2FFinanceManager-black?logo=github)](https://github.com/prashanth9894)

---

## 🧾 Overview

**Finance Manager & Investment Analyzer** is a web-based personal finance tracking system built with **Python (Django)**.  
It allows users to **manage income, expenses, and investments**, and visualize their financial data with interactive charts.

This project combines the features of a **Money Manager app** with an **Investment Analysis dashboard**, helping you make data-driven financial decisions.

---

## 🚀 Features

### 💵 Finance Tracking
- Add, edit, and delete **income** and **expense** records.  
- Categorize transactions for better insights.  
- Automatic balance and monthly summary calculation.  
- Export or import data in CSV format.

### 📊 Investment Analyzer
- Track mutual funds, SIPs, and custom investments.  
- Calculate **returns, profit/loss, CAGR, and diversification**.  
- Visualize portfolio growth with **Chart.js graphs**.  
- Compare investment performance over time.

### 🧮 Smart Analytics
- Expense vs Income ratio visualization.  
- Monthly and yearly financial reports.  
- Insights on top spending categories.  
- Total investment worth and asset allocation overview.



---

## 🧰 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | HTML, CSS, Bootstrap 5, Chart.js |
| **Backend** | Python, Django Framework |
| **Database** | SQLite (default) |
| **Version Control** | Git & GitHub |
| **Libraries** | Pandas, Matplotlib (optional) |

---

## 📁 Folder Structure

```

FinanceManager/
│
├── financeweb/                # Main Django project
│   ├── settings.py            # Project settings
│   ├── urls.py                # URL routing
│   ├── views.py               # Views and logic
│   ├── templates/             # HTML templates
│   └── static/                # CSS, JS, images
│
├── data/
│   └── transactions.csv       # Example data
│
├── db.sqlite3                 # Local database
├── manage.py                  # Django runner
├── requirements.txt           # Dependencies
└── README.md                  # Documentation

````

---

## ⚙️ Installation & Setup

### 🪜 Step 1: Clone the Repository
```bash
git clone https://github.com/prashanth9894/FinanceManager.git
cd FinanceManager
````

### 🧩 Step 2: Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate      # On Windows
source venv/bin/activate   # On macOS/Linux
```

### 📦 Step 3: Install Requirements

```bash
pip install -r requirements.txt
```

### 🏗️ Step 4: Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### ▶️ Step 5: Run the Server

```bash
python manage.py runserver
```

### 🌍 Step 6: Open in Browser

Visit: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🧠 Future Enhancements

* 💹 Live mutual fund API integration (Zerodha, Kotak, Groww).
* 📈 AI-based spending recommendations.
* 📤 Export reports as **PDF/Excel**.
* 📱 Mobile PWA version for on-the-go access.
* 🔔 Email/SMS alerts for goal tracking.
* 🧾 Expense predictions and category forecasts.

---

## 📸 Screenshots (Coming Soon)

| Dashboard       | Analytics       | Investment Overview |
| --------------- | --------------- | ------------------- |
| *(To be added)* | *(To be added)* | *(To be added)*     |

---

## 🤝 Contribution Guidelines

1. Fork the repository
2. Create a feature branch:

   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:

   ```bash
   git commit -m "Add new feature"
   ```
4. Push to your branch and open a Pull Request

---

## 👨‍💻 Developer

**Name:** [Prashanth N](https://www.linkedin.com/in/prashanth-n-b15792255)
**🌐 Portfolio:** [prashanth9894.github.io/imprashanth.github.io](https://prashanth9894.github.io/imprashanth.github.io/)
**📧 Email:** [prashanthnp9894@gmail.com](mailto:prashanthnp9894@gmail.com)
**💼 GitHub:** [@prashanth9894](https://github.com/prashanth9894)

---

## 🪪 License

This project is licensed under the [MIT License](LICENSE).
You are free to use, modify, and distribute it with proper attribution.

---

## 🌟 Support

If you like this project, please ⭐ **star the repo** and share it with others!
Your support motivates continued development 🚀

---

