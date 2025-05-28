from flask import Flask, request, render_template_string
import pandas as pd

app = Flask(__name__)
results = []

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Wingo 5 Minutes Analyzer</title>
</head>
<body>
    <h2>🎯 Wingo 5 Minutes Auto Analyzer</h2>
    <form method="post">
        <label>Color (red/green/violet):</label><br>
        <input type="text" name="color"><br><br>
        <label>Number (0-9):</label><br>
        <input type="number" name="number"><br><br>
        <input type="submit" value="Add Result">
    </form>
    <hr>
    {% if predictions %}
        <h3>🔍 Analysis Result:</h3>
        <pre>{{ predictions }}</pre>
    {% endif %}
</body>
</html>
"""

def analyze_results():
    if not results:
        return "No results yet."

    df = pd.DataFrame(results, columns=["Color", "Number"])
    df["Big/Small"] = df["Number"].apply(lambda x: "Big" if x >= 5 else "Small")
    df["Odd/Even"] = df["Number"].apply(lambda x: "Odd" if x % 2 == 1 else "Even")

    output = ""
    for col in ["Color", "Big/Small", "Odd/Even"]:
        counts = df[col].value_counts()
        total = len(df)
        pred = counts.idxmax()
        output += f"{col} → Likely: {pred.upper()}\n"
        for val, cnt in counts.items():
            pct = round(cnt / total * 100, 1)
            output += f"  {val}: {cnt} ({pct}%)\n"
        output += "\n"
    return output

@app.route("/", methods=["GET", "POST"])
def index():
    predictions = ""
    if request.method == "POST":
        color = request.form.get("color", "").strip().lower()
        try:
            number = int(request.form.get("number", ""))
            if color in ["red", "green", "violet"] and 0 <= number <= 9:
                results.append((color, number))
        except ValueError:
            pass
        predictions = analyze_results()
    return render_template_string(HTML_TEMPLATE, predictions=predictions)

if name == "__main__":
    app.run()
