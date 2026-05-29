import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "hydroplant.db")

# ── Critical limits for level alerts (in cm) ─────────────────────────────────
LEVEL_LIMITS = {
    "ug_spt":          {"min": 50,  "max": 280, "unit": "cm"},
    "grd_spt":         {"min": 50,  "max": 280, "unit": "cm"},
    "r1":              {"min": 50,  "max": 280, "unit": "cm"},
    "r2":              {"min": 50,  "max": 280, "unit": "cm"},
    "r3":              {"min": 50,  "max": 280, "unit": "cm"},
    "r4":              {"min": 50,  "max": 300, "unit": "cm"},
    "r5":              {"min": 50,  "max": 300, "unit": "cm"},
    "r6":              {"min": 50,  "max": 300, "unit": "cm"},
    "r7":              {"min": 50,  "max": 300, "unit": "cm"},
    "r8":              {"min": 50,  "max": 280, "unit": "cm"},
    "r9":              {"min": 50,  "max": 280, "unit": "cm"},
    "r10":             {"min": 50,  "max": 280, "unit": "cm"},
    "wr1":             {"min": 50,  "max": 200, "unit": "cm"},
    "wr2":             {"min": 50,  "max": 200, "unit": "cm"},
    "wr3":             {"min": 30,  "max": 200, "unit": "cm"},
    "wr4":             {"min": 50,  "max": 200, "unit": "cm"},
    "mlt01":           {"min": 50,  "max": 300, "unit": "cm"},
    "mlt02":           {"min": 50,  "max": 300, "unit": "cm"},
    "mlt03":           {"min": 50,  "max": 300, "unit": "cm"},
    "old_znso4":       {"min": 50,  "max": 400, "unit": "cm"},
    "new_znso4":       {"min": 50,  "max": 400, "unit": "cm"},
    "acid_storage":    {"min": 30,  "max": 300, "unit": "cm"},
    "acid_day_tank":   {"min": 20,  "max": 150, "unit": "cm"},
    "water_tank":      {"min": 30,  "max": 200, "unit": "cm"},
}

# ── Critical limits for acid (litres) ────────────────────────────────────────
ACID_LIMITS = {
    "acid_ug_spt":  {"max": 3000, "unit": "ltr"},
    "acid_grd_spt": {"max": 3000, "unit": "ltr"},
    "acid_r1":      {"max": 5000, "unit": "ltr"},
    "acid_r2":      {"max": 5000, "unit": "ltr"},
    "acid_r3":      {"max": 5000, "unit": "ltr"},
    "acid_r8":      {"max": 3000, "unit": "ltr"},
    "acid_r9":      {"max": 3000, "unit": "ltr"},
    "acid_r10":     {"max": 3000, "unit": "ltr"},
    "acid_wr03":    {"max": 1000, "unit": "ltr"},
}

# ── Critical limits for Zn dust (kg) ─────────────────────────────────────────
ZN_LIMITS = {
    "zn_r4": {"max": 2000, "unit": "kg"},
    "zn_r5": {"max": 2000, "unit": "kg"},
    "zn_r6": {"max": 2000, "unit": "kg"},
    "zn_r7": {"max": 2000, "unit": "kg"},
}

# ── Water consumption limit ───────────────────────────────────────────────────
WATER_LIMIT = {"max": 80, "unit": "m3"}

# Combined for alert checking
CRITICAL_LIMITS = {}
CRITICAL_LIMITS.update(LEVEL_LIMITS)
CRITICAL_LIMITS.update(ACID_LIMITS)
CRITICAL_LIMITS.update(ZN_LIMITS)


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    # ── Users ─────────────────────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'operator',
            full_name TEXT,
            shift TEXT,
            created_at TEXT DEFAULT (datetime('now','localtime'))
        )
    """)

    # ── Shift Report (main table) ──────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS shift_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            submitted_at TEXT DEFAULT (datetime('now','localtime')),
            report_date TEXT NOT NULL,

            -- Shift Info
            shift TEXT NOT NULL,
            shift_incharge_no TEXT,
            opt_filter TEXT,
            reactor_opt TEXT,
            helpers INTEGER DEFAULT 0,
            absent INTEGER DEFAULT 0,
            overtime INTEGER DEFAULT 0,
            near_miss INTEGER DEFAULT 0,

            -- PF Cake Charging (WMT)
            pf_g_spt REAL DEFAULT 0,
            pf_ug_spt REAL DEFAULT 0,

            -- Zn Dust Charging (kg)
            zn_r4 REAL DEFAULT 0,
            zn_r5 REAL DEFAULT 0,
            zn_r6 REAL DEFAULT 0,
            zn_r7 REAL DEFAULT 0,

            -- Acid (litres)
            acid_ug_spt REAL DEFAULT 0,
            acid_grd_spt REAL DEFAULT 0,
            acid_r1 REAL DEFAULT 0,
            acid_r2 REAL DEFAULT 0,
            acid_r3 REAL DEFAULT 0,
            acid_r8 REAL DEFAULT 0,
            acid_r9 REAL DEFAULT 0,
            acid_r10 REAL DEFAULT 0,
            acid_wr03 REAL DEFAULT 0,

            -- PAT & Lead Acetate (kg)
            pat_kg REAL DEFAULT 0,
            lead_acetate_kg REAL DEFAULT 0,

            -- Levels (cm) — tanks
            lvl_ug_spt REAL,
            lvl_grd_spt REAL,
            lvl_r1 REAL,
            lvl_r2 REAL,
            lvl_r3 REAL,
            lvl_r4 REAL,
            lvl_r5 REAL,
            lvl_r6 TEXT,   -- can be "E" (empty)
            lvl_r7 REAL,
            lvl_r8 REAL,
            lvl_r9 TEXT,   -- can be "E"
            lvl_r10 TEXT,  -- can be "E"
            lvl_wr1 REAL,
            lvl_wr2 REAL,
            lvl_wr3 REAL,
            lvl_wr4 REAL,
            lvl_mlt01 REAL,
            lvl_mlt02 REAL,
            lvl_mlt03 REAL,
            lvl_old_znso4 REAL,
            lvl_new_znso4 REAL,
            lvl_acid_storage REAL,
            lvl_acid_day_tank REAL,
            lvl_water REAL,

            -- Cake Output (WMT)
            cake_cu_cement REAL DEFAULT 0,
            cake_cd_sponge REAL DEFAULT 0,
            cake_co_cake REAL DEFAULT 0,

            -- Water Consumption
            water_consumption REAL DEFAULT 0,

            -- Remarks
            remarks TEXT,

            -- Meta
            submitted_by TEXT,
            has_warnings INTEGER DEFAULT 0
        )
    """)

    # ── Alerts log ────────────────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS alerts_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER,
            submitted_by TEXT,
            parameter TEXT,
            value REAL,
            limit_type TEXT,
            threshold REAL,
            severity TEXT,
            triggered_at TEXT DEFAULT (datetime('now','localtime')),
            resolved INTEGER DEFAULT 0,
            resolved_at TEXT,
            FOREIGN KEY (report_id) REFERENCES shift_reports(id)
        )
    """)

    # ── Audit log ─────────────────────────────────────────────────────────────
    cur.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            action TEXT,
            detail TEXT,
            ts TEXT DEFAULT (datetime('now','localtime'))
        )
    """)

    # ── Seed default users ────────────────────────────────────────────────────
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        defaults = [
            ("admin",     "admin123", "admin",    "Plant Administrator", "All"),
            ("incharge1", "shift123", "operator", "Ramesh Kumar",        "A"),
            ("incharge2", "shift456", "operator", "Priya Sharma",        "B"),
            ("incharge3", "shift789", "operator", "Vijay Singh",         "C"),
        ]
        cur.executemany(
            "INSERT INTO users (username,password,role,full_name,shift) VALUES (?,?,?,?,?)",
            defaults
        )

    conn.commit()
    conn.close()


# ── Insert helpers ─────────────────────────────────────────────────────────────

def insert_report(data: dict) -> int:
    conn = get_conn()
    cur = conn.cursor()
    cols = ", ".join(data.keys())
    placeholders = ", ".join(f":{k}" for k in data.keys())
    cur.execute(f"INSERT INTO shift_reports ({cols}) VALUES ({placeholders})", data)
    rid = cur.lastrowid
    conn.commit()
    conn.close()
    return rid


def insert_alerts(alerts: list):
    if not alerts:
        return
    conn = get_conn()
    cur = conn.cursor()
    cur.executemany("""
        INSERT INTO alerts_log
        (report_id, submitted_by, parameter, value, limit_type, threshold, severity)
        VALUES (:report_id, :submitted_by, :parameter, :value, :limit_type, :threshold, :severity)
    """, alerts)
    conn.commit()
    conn.close()


def log_audit(username, action, detail=""):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO audit_log (username,action,detail) VALUES (?,?,?)",
                (username, action, detail))
    conn.commit()
    conn.close()


# ── Read helpers ───────────────────────────────────────────────────────────────

def get_all_reports(limit=100):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM shift_reports ORDER BY submitted_at DESC LIMIT ?", (limit,))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def get_alerts(resolved=None, limit=200):
    conn = get_conn()
    cur = conn.cursor()
    if resolved is None:
        cur.execute("SELECT * FROM alerts_log ORDER BY triggered_at DESC LIMIT ?", (limit,))
    else:
        cur.execute("SELECT * FROM alerts_log WHERE resolved=? ORDER BY triggered_at DESC LIMIT ?",
                    (1 if resolved else 0, limit))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def resolve_alert(alert_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE alerts_log SET resolved=1, resolved_at=datetime('now','localtime') WHERE id=?",
                (alert_id,))
    conn.commit()
    conn.close()


def get_stats():
    conn = get_conn()
    cur = conn.cursor()
    stats = {}
    cur.execute("SELECT COUNT(*) as c FROM shift_reports")
    stats["total_reports"] = cur.fetchone()["c"]
    cur.execute("SELECT COUNT(*) as c FROM shift_reports WHERE submitted_at >= datetime('now','-24 hours','localtime')")
    stats["reports_24h"] = cur.fetchone()["c"]
    cur.execute("SELECT COUNT(*) as c FROM alerts_log WHERE resolved=0")
    stats["active_alerts"] = cur.fetchone()["c"]
    cur.execute("SELECT COUNT(*) as c FROM alerts_log WHERE severity='CRITICAL' AND resolved=0")
    stats["critical_alerts"] = cur.fetchone()["c"]
    conn.close()
    return stats


def get_all_users():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id,username,role,full_name,shift,created_at FROM users ORDER BY id")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def add_user(username, password, role, full_name, shift):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username,password,role,full_name,shift) VALUES (?,?,?,?,?)",
            (username, password, role, full_name, shift)
        )
        conn.commit()
        return True, "User created successfully"
    except sqlite3.IntegrityError:
        return False, "Username already exists"
    finally:
        conn.close()


def delete_user(user_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()


def change_password(username: str, old_password: str, new_password: str):
    """Verify old password then update to new password. Returns (success, message)."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username=? AND password=?", (username, old_password))
    row = cur.fetchone()
    if not row:
        conn.close()
        return False, "Current password is incorrect."
    cur.execute("UPDATE users SET password=? WHERE username=?", (new_password, username))
    conn.commit()
    conn.close()
    return True, "Password changed successfully."


def get_trend_data(field, days=7):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT report_date, submitted_at, {field}
        FROM shift_reports
        WHERE submitted_at >= datetime('now', ?, 'localtime')
        ORDER BY submitted_at ASC
    """, (f'-{days*24} hours',))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


# ── Alert checker ──────────────────────────────────────────────────────────────

def check_alerts_from_report(data: dict, report_id: int) -> list:
    alerts = []
    submitted_by = data.get("submitted_by", "")

    numeric_checks = {
        # Levels
        "lvl_ug_spt":        LEVEL_LIMITS.get("ug_spt"),
        "lvl_grd_spt":       LEVEL_LIMITS.get("grd_spt"),
        "lvl_r1":            LEVEL_LIMITS.get("r1"),
        "lvl_r2":            LEVEL_LIMITS.get("r2"),
        "lvl_r3":            LEVEL_LIMITS.get("r3"),
        "lvl_r4":            LEVEL_LIMITS.get("r4"),
        "lvl_r5":            LEVEL_LIMITS.get("r5"),
        "lvl_r7":            LEVEL_LIMITS.get("r7"),
        "lvl_r8":            LEVEL_LIMITS.get("r8"),
        "lvl_wr1":           LEVEL_LIMITS.get("wr1"),
        "lvl_wr2":           LEVEL_LIMITS.get("wr2"),
        "lvl_wr3":           LEVEL_LIMITS.get("wr3"),
        "lvl_wr4":           LEVEL_LIMITS.get("wr4"),
        "lvl_mlt01":         LEVEL_LIMITS.get("mlt01"),
        "lvl_mlt02":         LEVEL_LIMITS.get("mlt02"),
        "lvl_mlt03":         LEVEL_LIMITS.get("mlt03"),
        "lvl_old_znso4":     LEVEL_LIMITS.get("old_znso4"),
        "lvl_new_znso4":     LEVEL_LIMITS.get("new_znso4"),
        "lvl_acid_storage":  LEVEL_LIMITS.get("acid_storage"),
        "lvl_acid_day_tank": LEVEL_LIMITS.get("acid_day_tank"),
        "lvl_water":         LEVEL_LIMITS.get("water_tank"),
        # Acid
        "acid_ug_spt":  ACID_LIMITS.get("acid_ug_spt"),
        "acid_grd_spt": ACID_LIMITS.get("acid_grd_spt"),
        "acid_r1":      ACID_LIMITS.get("acid_r1"),
        "acid_r2":      ACID_LIMITS.get("acid_r2"),
        "acid_r3":      ACID_LIMITS.get("acid_r3"),
        "acid_r8":      ACID_LIMITS.get("acid_r8"),
        "acid_r9":      ACID_LIMITS.get("acid_r9"),
        "acid_r10":     ACID_LIMITS.get("acid_r10"),
        "acid_wr03":    ACID_LIMITS.get("acid_wr03"),
        # Zn dust
        "zn_r4": ZN_LIMITS.get("zn_r4"),
        "zn_r5": ZN_LIMITS.get("zn_r5"),
        "zn_r6": ZN_LIMITS.get("zn_r6"),
        "zn_r7": ZN_LIMITS.get("zn_r7"),
        # Water
        "water_consumption": WATER_LIMIT,
    }

    for field, limits in numeric_checks.items():
        if limits is None:
            continue
        val = data.get(field)
        try:
            val = float(val)
        except (TypeError, ValueError):
            continue

        min_v = limits.get("min")
        max_v = limits.get("max")
        unit  = limits.get("unit", "")
        label = field.replace("lvl_", "LEVEL ").replace("_", " ").upper()

        if min_v is not None and val < min_v:
            pct = abs(val - min_v) / (min_v + 0.001) * 100
            alerts.append({
                "report_id":    report_id,
                "submitted_by": submitted_by,
                "parameter":    label,
                "value":        val,
                "limit_type":   f"LOW (min {min_v} {unit})",
                "threshold":    min_v,
                "severity":     "CRITICAL" if pct > 20 else "WARNING",
            })
        elif max_v is not None and val > max_v:
            pct = abs(val - max_v) / (max_v + 0.001) * 100
            alerts.append({
                "report_id":    report_id,
                "submitted_by": submitted_by,
                "parameter":    label,
                "value":        val,
                "limit_type":   f"HIGH (max {max_v} {unit})",
                "threshold":    max_v,
                "severity":     "CRITICAL" if pct > 20 else "WARNING",
            })

    return alerts
