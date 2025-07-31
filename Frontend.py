from flask import Flask, render_template, request
import requests
import base64

app = Flask(__name__)
FASTAPI_URL = "http://localhost:8000/predict"

@app.route("/", methods=["GET", "POST"])
def upload_file():
    prediction_img = None
    input_img = None
    error = None
    channels_img=None

    if request.method == "POST":
        file = request.files["file"]
        if not file:
            error = "No file selected!"
        else:
            try:
                file_bytes = file.read()
                input_img = base64.b64encode(file_bytes).decode("utf-8")
                file.stream.seek(0)
                response = requests.post(
                    FASTAPI_URL,
                    files={"file": (file.filename, file.stream, file.mimetype)}
                )
                data = response.json()

                if response.status_code == 200 and "image_base64" in data and "channels_base64" in data:
                    prediction_img = data["image_base64"]
                    channels_img = data["channels_base64"]
                else:
                    error = data.get("error", "Prediction failed.")
            except Exception as e:
                error = str(e)

    return render_template("index.html", input_img=input_img, prediction_img=prediction_img, error=error,channels_img=channels_img)

if __name__ == "__main__":
    app.run(debug=True)
