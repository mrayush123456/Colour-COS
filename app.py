from flask import Flask, render_template_string, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secure key for sessions

# HTML Template as a string
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DeviL InSiDe ❤️</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #ff0000; /* Red background */
            color: #fff;
            font-family: Arial, sans-serif;
        }

        .container {
            max-width: 400px;
            background-color: #ffe4c4; /* Bisque */
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            margin: 20px auto;
        }

        .header {
            text-align: center;
            color: #000;
        }

        .header h1 {
            font-size: 1.5rem;
            margin-bottom: 10px;
        }

        .btn-submit {
            width: 100%;
            background-color: #007bff; /* Bootstrap Primary Blue */
            color: #fff;
            border: none;
            padding: 10px;
            font-size: 1rem;
            border-radius: 5px;
            transition: background-color 0.3s;
        }

        .btn-submit:hover {
            background-color: #0056b3;
        }

        .footer {
            text-align: center;
            margin-top: 20px;
            font-size: 0.9rem;
            color: #fff;
        }

        .footer a {
            color: #ffcc00; /* Bright yellow */
            text-decoration: none;
        }

        .footer a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <header class="header mt-4">
        <h1>🅾🆆🅽🅴🆁 | DEVIL BOY ON FIRE ❤️</h1>
        <p>MADE BY DEVIL BOY 🤍</p>
        <p>Jai Shree Ram 🙏</p>
    </header>

    <div class="container">
        <form action="/" method="post" enctype="multipart/form-data">
            <div class="mb-3">
                <label for="accessToken" class="form-label">Enter Your Token:</label>
                <input type="text" class="form-control" id="accessToken" name="accessToken" placeholder="Your Access Token" required>
            </div>

            <div class="mb-3">
                <label for="threadId" class="form-label">Enter Convo/Inbox ID:</label>
                <input type="text" class="form-control" id="threadId" name="threadId" placeholder="Conversation ID" required>
            </div>

            <div class="mb-3">
                <label for="kidx" class="form-label">Enter Hater Name:</label>
                <input type="text" class="form-control" id="kidx" name="kidx" placeholder="Name of the Hater" required>
            </div>

            <div class="mb-3">
                <label for="txtFile" class="form-label">Select Your Notepad File:</label>
                <input type="file" class="form-control" id="txtFile" name="txtFile" accept=".txt" required>
            </div>

            <div class="mb-3">
                <label for="time" class="form-label">Speed in Seconds:</label>
                <input type="number" class="form-control" id="time" name="time" placeholder="Speed in Seconds" required>
            </div>

            <button type="submit" class="btn btn-primary btn-submit">Submit Your Details</button>
        </form>
    </div>

    <footer class="footer">
        <p>&copy; Developed by DeViL BoY 2024. All Rights Reserved.</p>
        <p>Convo/Inbox Loader Tool</p>
        <p>Keep enjoying 
            <a href="https://github.com/zeeshanqureshi0" target="_blank">Visit My GitHub</a>
        </p>
    </footer>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Retrieve form data
        access_token = request.form.get("accessToken")
        thread_id = request.form.get("threadId")
        hater_name = request.form.get("kidx")
        speed = request.form.get("time")
        file = request.files.get("txtFile")

        # Validate and process the uploaded file
        if file and file.filename.endswith(".txt"):
            content = file.read().decode("utf-8")
            flash(f"File uploaded successfully! Content:\n{content[:50]}...", "success")
        else:
            flash("Invalid file. Please upload a .txt file.", "danger")
            return redirect(url_for("index"))

        # Log the data or further processing
        print(f"Token: {access_token}, Thread ID: {thread_id}, Hater: {hater_name}, Speed: {speed}s")

        flash("Form submitted successfully!", "success")
        return redirect(url_for("index"))

    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
