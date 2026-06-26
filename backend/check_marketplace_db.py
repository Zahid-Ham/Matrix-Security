import sqlite3
conn = sqlite3.connect('matrix.db')
tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print("All tables:", tables)

# Check valuation-related tables
for t in tables:
    if 'valuat' in t.lower() or 'marketplace' in t.lower():
        print(f"\nTable '{t}' row count:", conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0])

# Check vulnerability marketplace columns
print("\nVulnerability table marketplace columns:")
print(conn.execute("SELECT id, title, marketplace_value_avg, marketplace_last_analyzed FROM vulnerabilities WHERE marketplace_value_avg IS NOT NULL LIMIT 5").fetchall())
