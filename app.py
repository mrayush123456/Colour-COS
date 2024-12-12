from flask import Flask, request, render_template_string, flash, redirect, url_for
from fbchat import Client
from fbchat.models import Message, ThreadType
import time
import threading

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Global flag to stop sending messages
stop_flag = False

# HTML template for the Flask app
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
            background: linear-gradient(to right, #ff9966, #ff5e62);
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
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
            width: 400px;
            text-align: center;
        }
        h1 {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin: 10px 0 5px;
        }
        input, button {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            background-color: #28a745;
            color: white;
            font-weight: bold;
        }
        button:hover {
            background-color: #218838;
        }
        .stop-button {
            background-color: #dc3545;
        }
        .stop-button:hover {
            background-color: #c82333;
        }
        .message {
            margin-top: 10px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Facebook Messenger Automation</h1>
        <form action="/" method="POST" enctype="multipart/form-data">
            <label for="cookie">Session Cookie (c_user & xs):</label>
            <input type="text" id="cookie" name="cookie" placeholder="Paste your session cookie here" required>

            <label for="targets">Target IDs (comma-separated):</label>
            <input type="text" id="targets" name="targets" placeholder="Enter target user/group IDs" required>

            <label for="message_file">Message File:</label>
            <input type="file" id="message_file" name="message_file" accept=".txt" required>

            <label for="delay">Delay (in seconds):</label>
            <input type="number" id="delay" name="delay" placeholder="Enter delay between messages" required>

            <button type="submit">Start Sending</button>
        </form>
        <form action="/stop" method="POST">
            <button type="submit" class="stop-button">Stop Sending</button>
        </form>
    </div>
</body>
</html>
'''

# Function to send messages
def send_messages(cookie, targets, messages, delay):
    global stop_flag
    stop_flag = False
    try:
        # Parse the cookie string into a dictionary
        cookie_dict = dict(item.split("=") for item in cookie.split("; "))
        client = Client('', '', session_cookies=cookie_dict)

        # Split target IDs into a list
        target_list = targets.split(",")

        # Iterate over targets and messages
        for target in target_list:
            if stop_flag:
                print("[INFO] Stopping message sending...")
                break

            for message in messages:
                if stop_flag:
                    print("[INFO] Stopping message sending...")
                    break

                # Send message
                print(f"[INFO] Sending message to {target.strip()}: {message}")
                client.send(
                    Message(text=message),
                    thread_id=target.strip(),
                    thread_type=ThreadType.USER if target.strip().isdigit() else ThreadType.GROUP,
                )
                print(f"[SUCCESS] Message sent to {target.strip()}: {message}")
                time.sleep(delay)

        if not stop_flag:
            print("[INFO] All messages sent successfully!")
        client.logout()

    except Exception as e:
        print(f"[ERROR] {e}")

# Flask route for the home page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        global stop_flag
        stop_flag = False
        try:
            # Retrieve form data
            cookie = request.form["cookie"]
            targets = request.form["targets"]
            delay = int(request.form["delay"])
            message_file = request.files["message_file"]

            # Read messages from the uploaded file
            messages = message_file.read().decode("utf-8").splitlines()
            if not messages:
                flash("Message file is empty!", "error")
                return redirect(url_for("index"))

            # Start sending messages in a background thread
            threading.Thread(target=send_messages, args=(cookie, targets, messages, delay)).start()
            flash("Messages are being sent in the background.", "success")

        except Exception as e:
            flash(f"An error occurred: {e}", "error")

    return render_template_string(HTML_TEMPLATE)

# Flask route to stop message sending
@app.route("/stop", methods=["POST"])
def stop():
    global stop_flag
    stop_flag = True
    flash("Message sending has been stopped.", "info")
    return redirect(url_for("index"))

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
