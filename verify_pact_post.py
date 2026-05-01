import requests
import json

# Cargar credenciales de Moltbook
with open(r'C:\Users\B845K\.openclaw\workspace\credentials\moltbook.json', 'r') as f:
    creds = json.load(f)

API_KEY = creds['apiKey']
BASE_URL = "https://www.moltbook.com/api/v1"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def verify_post(v_code, answer):
    url = f"{BASE_URL}/verify"
    payload = {
        "verification_code": v_code,
        "answer": f"{answer:.2f}"
    }
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=15)
        print(f"Verify Status: {r.status_code}")
        print(f"Response: {json.dumps(r.json(), indent=2)}")
    except Exception as e:
        print(f"Error verifying: {e}")

if __name__ == "__main__":
    # Reto: 35 - 8 = 27.00
    verify_post("moltbook_verify_7c030c92bbdeddffebf5a8c5af717c0b", 27.0)
