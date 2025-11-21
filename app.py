import os
from flask import Flask, request, render_template, jsonify, send_file
from dotenv import load_dotenv
import openpyxl
from io import BytesIO
from generator.ai_generator import generate_test_case

load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    story = data.get("user_story")
    url = data.get("url")
    tc_type = data.get("tc_type")
    result = generate_test_case(story, url, tc_type)
    return jsonify(result)

@app.route("/download_excel", methods=["POST"])
def download_excel():
    data = request.json
    tc = data.get("testcase")

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Test Case"

    ws.append(["ID","Title","Type","Priority","Preconditions","Steps","Expected Result"])

    ws.append([
        tc["id"],
        tc["title"],
        tc["type"],
        tc["priority"],
        tc["preconditions"],
        "\n".join(tc["steps"]),
        tc["expected_result"]
    ])

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(output, download_name="testcase.xlsx", as_attachment=True)

if __name__ == "__main__":
    # When deployed on Render use PORT environment variable and 0.0.0.0
    import os
    debug = os.getenv("FLASK_DEBUG", "False").lower() in ("1","true","yes")
    host = "0.0.0.0"
    port = int(os.getenv("PORT", os.getenv("FLASK_PORT", 5000)))
    app.run(debug=debug, host=host, port=port)

