"""
Script to trigger marketplace backfill on production server.
Logs in, gets auth token, then calls the backfill endpoint.
"""
import urllib.request
import urllib.parse
import json
import sys

BASE_URL = "https://matrix-backend-2jgz.onrender.com"

# Step 1: Login to get auth token
print("[1] Logging in to production server...")
login_data = json.dumps({
    "username": "admin",
    "password": "admin"
}).encode()

# Try login endpoint
try:
    req = urllib.request.Request(
        f"{BASE_URL}/api/auth/login",
        data=login_data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode())
        print("Login response:", result)
except Exception as e:
    print(f"Login error: {e}")
    
    # Try form-based login (OAuth2PasswordRequestForm)
    print("\n[1b] Trying form-based login...")
    form_data = urllib.parse.urlencode({
        "username": "admin",
        "password": "admin"
    }).encode()
    
    try:
        req2 = urllib.request.Request(
            f"{BASE_URL}/api/auth/token",
            data=form_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST"
        )
        with urllib.request.urlopen(req2, timeout=30) as resp2:
            result = json.loads(resp2.read().decode())
            print("Form login response:", result)
    except Exception as e2:
        print(f"Form login also failed: {e2}")
        sys.exit(1)
