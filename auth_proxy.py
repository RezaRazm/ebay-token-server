from flask import Flask, jsonify, request
import requests
import base64
import os

app = Flask(__name__)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"

# eBay full scope set: All Selling + Buying APIs
SCOPES = [
    "https://api.ebay.com/oauth/api_scope",
    "https://api.ebay.com/oauth/api_scope/buy.marketing",
    "https://api.ebay.com/oauth/api_scope/buy.product.feed",
    "https://api.ebay.com/oauth/api_scope/buy.product.identification",
    "https://api.ebay.com/oauth/api_scope/buy.product.summary",
    "https://api.ebay.com/oauth/api_scope/buy.item.feed",
    "https://api.ebay.com/oauth/api_scope/buy.item.summary",
    "https://api.ebay.com/oauth/api_scope/buy.item.auction",
    "https://api.ebay.com/oauth/api_scope/buy.item",
    "https://api.ebay.com/oauth/api_scope/buy.guest.order",
    "https://api.ebay.com/oauth/api_scope/commerce.catalog.readonly",
    "https://api.ebay.com/oauth/api_scope/commerce.identity.readonly",
    "https://api.ebay.com/oauth/api_scope/commerce.identity.email.readonly",
    "https://api.ebay.com/oauth/api_scope/commerce.notification.subscription",
    "https://api.ebay.com/oauth/api_scope/commerce.notification.subscription.readonly",
    "https://api.ebay.com/oauth/api_scope/sell.account",
    "https://api.ebay.com/oauth/api_scope/sell.account.readonly",
    "https://api.ebay.com/oauth/api_scope/sell.inventory",
    "https://api.ebay.com/oauth/api_scope/sell.inventory.readonly",
    "https://api.ebay.com/oauth/api_scope/sell.fulfillment",
    "https://api.ebay.com/oauth/api_scope/sell.fulfillment.readonly",
    "https://api.ebay.com/oauth/api_scope/sell.payment.dispute",
    "https://api.ebay.com/oauth/api_scope/sell.reputation",
    "https://api.ebay.com/oauth/api_scope/sell.reputation.readonly",
    "https://api.ebay.com/oauth/api_scope/sell.analytics.readonly",
    "https://api.ebay.com/oauth/api_scope/sell.marketing",
    "https://api.ebay.com/oauth/api_scope/sell.marketing.readonly",
    "https://api.ebay.com/oauth/api_scope/sell.finances",
    "https://api.ebay.com/oauth/api_scope/sell.stores",
    "https://api.ebay.com/oauth/api_scope/sell.stores.readonly",
    "https://api.ebay.com/oauth/api_scope/sell.negotiation",
    "https://api.ebay.com/oauth/api_scope/sell.metadata",
    "https://api.ebay.com/oauth/api_scope/sell.edelivery"
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
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
