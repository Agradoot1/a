
from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)
df = pd.read_csv("data.csv")

@app.route("/summary")
def summary():
    return jsonify(df.describe().to_dict())

@app.route("/filter", methods=["POST"])
def filter_data():
    condition = request.json.get("condition")
    try:
        filtered_df = df.query(condition)
        return filtered_df.to_json(orient="records")
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/groupby/<column>")
def groupby(column):
    if column not in df.columns:
        return jsonify({"error": "Column not found"}), 404
    return jsonify(df.groupby(column).mean().to_dict())

if __name__ == "__main__":
    app.run(debug=True)
