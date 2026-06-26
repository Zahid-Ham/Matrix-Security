import sqlite3

conn = sqlite3.connect('matrix.db')
cursor = conn.cursor()

print("--- USERS ---")
users = cursor.execute("SELECT id, username, email FROM users").fetchall()
for u in users:
    print(f"User ID: {u[0]}, Username: {u[1]}, Email: {u[2]}")

print("\n--- SCANS ---")
scans = cursor.execute("SELECT id, user_id, target_url, target_name, status, created_at FROM scans").fetchall()
for s in scans:
    print(f"Scan ID: {s[0]}, User ID: {s[1]}, Target: {s[2]} ({s[3]}), Status: {s[4]}, Created: {s[5]}")

print("\n--- VULNERABILITIES ---")
vulns = cursor.execute("SELECT id, scan_id, title, severity, marketplace_value_avg FROM vulnerabilities").fetchall()
print(f"Total vulnerabilities: {len(vulns)}")
print("Vulnerabilities sample:")
for v in vulns[:15]:
    print(f"ID: {v[0]}, Scan ID: {v[1]}, Title: {v[2]}, Severity: {v[3]}, Valued: {v[4]}")
