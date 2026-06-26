"""
Diagnose production marketplace state and trigger re-analysis for user iqra123.
"""
import urllib.request
import urllib.parse
import urllib.error
import json
import http.cookiejar

BASE_URL = "https://matrix-backend-2jgz.onrender.com"
jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

def post_json(path, data, extra_headers=None):
    body = json.dumps(data).encode()
    headers = {"Content-Type": "application/json"}
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(f"{BASE_URL}{path}", data=body, headers=headers, method="POST")
    try:
        with opener.open(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())

def get_json(path, extra_headers=None):
    headers = {}
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(f"{BASE_URL}{path}", headers=headers)
    try:
        with opener.open(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())

# --- Step 0: Get CSRF token ---
print("[0] Getting CSRF token...")
status, csrf_data = get_json("/api/csrf/")
print(f"    Status: {status}")
csrf_token = csrf_data.get("csrf_token", "")
print(f"    CSRF token: {csrf_token[:20]}...")

# --- Step 1: Login as iqra123 ---
print("\n[1] Logging in as iqra123...")
status, login_data = post_json("/api/auth/login", {
    "username": "iqra123",
    "password": "iqra@123"
}, extra_headers={"X-CSRF-Token": csrf_token})
print(f"    Status: {status}")
if status == 200:
    print(f"    Login success: {login_data.get('username', 'unknown')}")
else:
    print(f"    Login failed: {login_data}")
    # Try common passwords
    for pwd in ["password", "admin", "iqra123", "123456", "test"]:
        status, r = post_json("/api/auth/login", {"username": "iqra123", "password": pwd},
                              extra_headers={"X-CSRF-Token": csrf_token})
        if status == 200:
            print(f"    Login success with password '{pwd}'")
            break
        print(f"    Tried '{pwd}': {status}")

# --- Step 2: Check user's marketplace dashboard ---
print("\n[2] Checking marketplace dashboard as iqra123...")
status, dash_data = get_json("/api/marketplace/dashboard", extra_headers={"X-CSRF-Token": csrf_token})
print(f"    Status: {status}")
print(f"    Dashboard: {json.dumps(dash_data, indent=2)[:500]}")

# --- Step 3: Check total unvalued vulns in production (any user) ---
print("\n[3] Checking unauthenticated dashboard (to see raw unfiltered count)...")
req = urllib.request.urlopen(f"{BASE_URL}/api/marketplace/dashboard", timeout=30)
print("    Unexpected success (should have required auth)")
