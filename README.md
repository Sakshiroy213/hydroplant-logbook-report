# ⚡ HydroPlant Reactor Monitoring System

A full-featured **Streamlit + SQLite** web application for hydro plant shift incharges to record and monitor reactor parameters in real time.

---

## 🚀 QUICK START

### 1. Install Python 3.9+
Download from https://www.python.org/downloads/

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```
Open your browser at: **http://localhost:8501**

---

## 🔑 DEFAULT LOGIN CREDENTIALS

| Username    | Password   | Role     | Shift     |
|-------------|------------|----------|-----------|
| `admin`     | `admin123` | Admin    | All       |
| `incharge1` | `shift123` | Operator | Morning   |
| `incharge2` | `shift456` | Operator | Afternoon |
| `incharge3` | `shift789` | Operator | Night     |

---

## 📦 PROJECT STRUCTURE

```
hydroplant/
├── app.py                  # Main entry point + login + routing
├── requirements.txt        # Python dependencies
├── hydroplant.db           # SQLite database (auto-created)
├── .streamlit/
│   └── config.toml         # Dark theme config
├── pages/
│   ├── data_entry.py       # Shift incharge data entry form
│   ├── dashboard.py        # Admin overview dashboard
│   ├── alerts.py           # Alerts & warnings log (admin only)
│   ├── trends.py           # Trend charts (admin only)
│   └── users.py            # User management (admin only)
└── utils/
    ├── db.py               # Database layer + critical limits
    └── auth.py             # Login authentication
```

---

## 🔬 PARAMETERS TRACKED

| Parameter         | Unit    | Min Limit | Max Limit |
|-------------------|---------|-----------|-----------|
| pH                | pH      | 6.5       | 8.5       |
| Acid Added        | L       | 0.5       | 10.0      |
| Temperature       | °C      | 15.0      | 45.0      |
| Pressure          | bar     | 1.0       | 6.0       |
| Flow Rate         | L/min   | 10.0      | 200.0     |
| Dissolved Oxygen  | mg/L    | 5.0       | 12.0      |
| Turbidity         | NTU     | 0.0       | 4.0       |
| Chlorine          | mg/L    | 0.2       | 2.0       |
| Conductivity      | µS/cm   | 50.0      | 800.0     |
| Water Level       | %       | 20.0      | 95.0      |

---

## 🚨 ALERT SYSTEM

- **WARNING**: Parameter exceeds limit by up to 20%
- **CRITICAL**: Parameter exceeds limit by more than 20%
- Alerts are **NEVER shown** to shift incharges on the entry form
- Alerts only appear in the **Admin Dashboard → Alerts & Warnings** page
- Admins can **resolve** alerts manually once investigated

---

## 🗄️ DATABASE TABLES

### `reactor_readings`
All submitted readings with timestamps, operator info, and all parameters.

### `alerts_log`
Auto-generated alert records for every parameter breach.

### `users`
Login credentials and roles for all plant personnel.

---

## 🛡️ SECURITY NOTE

Passwords are stored in plain text for this demo version.  
For production deployment, replace with **bcrypt** or **Argon2** password hashing:
```bash
pip install bcrypt
```

---

## 📈 FEATURES

- ✅ Role-based access (Admin / Operator)
- ✅ 8 reactor support
- ✅ Auto-timestamped submissions
- ✅ 10 physical/chemical parameters per reactor
- ✅ Automatic breach detection with WARNING/CRITICAL levels
- ✅ Admin-only alert dashboard (hidden from operators)
- ✅ Trend charts per reactor per parameter
- ✅ Multi-parameter comparison (normalized)
- ✅ CSV export of readings and alerts
- ✅ User management (add/remove operators)
- ✅ Auto shift detection based on current time
- ✅ Dark industrial UI theme

---

## 🔧 CUSTOMIZING CRITICAL LIMITS

Edit `utils/db.py` → `CRITICAL_LIMITS` dictionary:

```python
CRITICAL_LIMITS = {
    "ph": {"min": 6.5, "max": 8.5, "unit": "pH"},
    "temperature": {"min": 15.0, "max": 45.0, "unit": "°C"},
    # ... add or modify as needed
}
```
