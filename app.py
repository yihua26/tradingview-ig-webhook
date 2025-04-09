from flask import Flask, request, jsonify
from ig_client import IGClient

app = Flask(__name__)
ig = IGClient()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("📩 Webhook received:", data)

    signal = data.get('signal')  # e.g. {"signal": "buy", "symbol": "CS.D.USDJPY.CFD.IP"}

    if not signal:
        return jsonify({"error": "No signal provided"}), 400

    if signal == "buy":
        result = ig.place_order("BUY", data.get("symbol", "CS.D.USDJPY.CFD.IP"), 1)
    elif signal == "sell":
        result = ig.place_order("SELL", data.get("symbol", "CS.D.USDJPY.CFD.IP"), 1)
    else:
        return jsonify({"error": "Unknown signal"}), 400

    return jsonify({"status": "success", "response": result})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)