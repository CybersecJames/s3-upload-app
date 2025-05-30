# 01
from flask import Flask, request, redirect, render_template

# 02
import boto3
import os

# 03
app = Flask(__name__)

# 04
S3_BUCKET = os.environ.get("S3_BUCKET_NAME")
s3 = boto3.client("s3")

# 05
@app.route("/", methods=["GET"])
def upload_form():
    return render_template("upload.html")

# 06
@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    if file.filename != "":
        s3.upload_fileobj(file, S3_BUCKET, file.filename)
    return redirect("/")

# 07
@app.route("/files")
def list_files():
    objects = s3.list_objects_v2(Bucket=S3_BUCKET).get("Contents", [])
    urls = [f"https://{S3_BUCKET}.s3.amazonaws.com/{obj['Key']}" for obj in objects]
    return "<br>".join(urls)

# 08
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
