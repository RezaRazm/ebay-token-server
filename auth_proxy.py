from flask import Flask, jsonify
import requests
import base64
import os

app = Flask(__name__)

# Your eBay production credentials
CLIENT_ID = "RezaRazm-Sanbox-PRD-4abfbb41d-bb26fcf4"
CLIENT_SECRET = "PRD-476d66721f2d-b88b-48c3-90e5-da59"
REFRESH_TOKEN = "v^1.1#i^1#r^1#p^3#f^0#I^3#t^Ul4xMF8xMDozMzdFMDhBN0RFNkUyRTBFNDYzNjMxNTM3QzgzOTJGOV8xXzEjRV4yNjA="
TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"

# ✅ Safe, minimal set of scopes for testing
SCOPES = [
    "https://api.ebay.com/oauth/api_scope",
    "https://api.ebay.com/oauth/api_scope/sell.inventory"
]

@app.route("/get-token", methods=["GET"])
def get_token():
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {auth_header}"
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "scope": " ".join(SCOPES)
    }
    response = requests.post(TOKEN_URL, headers=headers, data=data)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to refresh token", "details": response.text}), response.status_code

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    app.run(debug=True, host="0.0.0.0", port=port)
