from flask import Flask, render_template, request
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import FormRecognizerClient

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"  # Change this to a secure secret key

key = "127a6d9b2e05462883d9885566908b8a"
endpoint = "https://analyzepdfs.cognitiveservices.azure.com/"
fileLocale = "en-US"
fileModelID = 'prebuilt-invoice'

credential = AzureKeyCredential(key)
form_recognizer_client = FormRecognizerClient(endpoint, credential)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename.endswith(".pdf"):
            # Analyze the uploaded PDF
            poller = form_recognizer_client.begin_recognize_content(file.stream)
            result = poller.result()

            # Extracted information
            cell_contents = []

            for page in result:
                for table in page.tables:
                    for cell in table.cells:
                        cell_contents.append(cell.text)

            print("Cell Contents:", cell_contents)  # Debugging line

            return render_template("result.html", cell_contents=cell_contents)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
