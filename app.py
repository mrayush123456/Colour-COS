from flask import Flask, request, render_template_string, flash, redirect, url_for
import time
import threading
import requests

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Global variable to control the stop button functionality
stop_sending = False

# HTML Template with a colorful background and stop button
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Messenger Automation</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to right, #ff7e5f, #feb47b);
            color: white;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: rgba(0, 0, 0, 0.8);
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            max-width: 500px;
            width: 100%;
        }
        h1 {
            text-align: center;
            color: #ffcccb;
        }
        label {
            display: block;
            margin: 10px 0 5px;
            font-weight: bold;
        }
        input, button {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
        }
        input[type="text"], input[type="password"], input[type="number"], input[type="file"] {
            background-color: #f0f0f0;
        }
        button {
            background-color: #ff5f57;
            color: white;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover {
            background-color: #ff3b30;
        }
        .stop-btn {
            background-color: #333;
            color: white;
            font-size: 14px;
            margin-top: 10px;
        }
        .stop-btn:hover {
            background-color: #555;
        }
        .message {
            text-align: center;
            font-size: 14px;
            margin-top: 10px;
        }
        .success {
            color: green;
        }
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Messenger Automation</h1>
        <form action="/" method="POST" enctype="multipart/form-data">
            <label for="token">Facebook Token:</label>
            <input type="text" id="token" name="token" placeholder="Paste your token here" required>

            <label for="target_id">Target Group/Inbox ID:</label>
            <input type="text" id="target_id" name="target_id" placeholder="Enter target chat ID" required>

            <label for="message_file">Message File (TXT):</label>
            <input type="file" id="message_file" name="message_file" accept=".txt" required>

            <label for="delay">Delay (in seconds):</label>
            <input type="number" id="delay" name="delay" placeholder="Enter delay between messages" required>

            <button type="submit">Send Messages</button>
        </form>
        <form action="/stop" method="POST">
            <button type="submit" class="stop-btn">Stop Sending</button>
        </form>
        {% with messages = get_flashed_messages(with_categories=True) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="message {{ category }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
        {% endwith %}
    </div>
</body>
</html>
'''

# Function to send messages in a thread
def send_messages(token, target_id, messages, delay):
    global stop_sending
    stop_sending = False
    try:
        for message in messages:
            if stop_sending:
                print("[INFO] Sending stopped by the user.")
                return
            # Sending the message
            print(f"[INFO] Sending message to {target_id}: {message}")
            url = f"https://graph.facebook.com/v16.0/{target_id}/messages"
            payload = {"message": message}
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(url, json=payload, headers=headers)

            # Log response
            if response.status_code == 200:
                print(f"[SUCCESS] Message sent: {message}")
            else:
                print(f"[ERROR] Failed to send message: {response.text}")

            time.sleep(delay)
        print("[INFO] All messages sent successfully!")
    except Exception as e:
        print(f"[ERROR] Exception occurred: {e}")

# Flask route for the main page
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            # Get form data
            token = request.form["token"]
            target_id = request.form["target_id"]
            delay = int(request.form["delay"])
            message_file = request.files["message_file"]

            # Read messages from the file
            messages = message_file.read().decode("utf-8").splitlines()
            if not messages:
                flash("Message file is empty!", "error")
                return redirect(url_for("home"))

            # Start a thread to send messages
            threading.Thread(target=send_messages, args=(token, target_id, messages, delay)).start()
            flash("Messages are being sent!", "success")
        except Exception as e:
            flash(f"An error occurred: {e}", "error")

    return render_template_string(HTML_TEMPLATE)

# Route to stop the message-sending process
@app.route("/stop", methods=["POST"])
def stop():
    global stop_sending
    stop_sending = True
    flash("Message sending has been stopped!", "success")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
        
