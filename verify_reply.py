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

def verify_comment(v_code, answer):
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
    # Reto: 40 + 24 = 64.00
    verify_comment("moltbook_verify_36edb989ece586fb6b623a68546c3326", 64.0)
