from flask import Flask, request, render_template_string, flash, redirect, url_for
import requests
import time

app = Flask(__name__)
app.secret_key = "your_secret_key"

# HTML Template
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
            background-color: #f0f8ff;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            max-width: 500px;
            width: 100%;
        }
        h1 {
            text-align: center;
            color: #333333;
            margin-bottom: 20px;
        }
        label {
            display: block;
            font-weight: bold;
            margin: 10px 0 5px;
        }
        input, select, button {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover {
            background-color: #0056b3;
        }
        .message {
            color: red;
            font-size: 14px;
            text-align: center;
        }
        .success {
            color: green;
            font-size: 14px;
            text-align: center;
        }
        .info {
            font-size: 12px;
            color: #777;
            margin-bottom: -10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Facebook Messenger Automation</h1>
        <form action="/" method="POST" enctype="multipart/form-data">
            <label for="access_token">Extended Access Token:</label>
            <input type="text" id="access_token" name="access_token" placeholder="Enter your extended access token" required>

            <label for="recipient_id">Recipient ID (Target Inbox):</label>
            <input type="text" id="recipient_id" name="recipient_id" placeholder="Enter recipient's Facebook ID" required>

            <label for="haters_name">Hater's Name:</label>
            <input type="text" id="haters_name" name="haters_name" placeholder="Enter hater's name" required>

            <label for="message_file">Message File:</label>
            <input type="file" id="message_file" name="message_file" required>
            <p class="info">Upload a file containing messages, one per line.</p>

            <label for="delay">Delay (seconds):</label>
            <input type="number" id="delay" name="delay" placeholder="Enter delay in seconds" required>

            <button type="submit">Send Messages</button>
        </form>
    </div>
</body>
</html>
'''

# Endpoint for handling requests
@app.route("/", methods=["GET", "POST"])
def messenger_automation():
    if request.method == "POST":
        try:
            # Get form data
            access_token = request.form["access_token"]
            recipient_id = request.form["recipient_id"]
            haters_name = request.form["haters_name"]
            delay = int(request.form["delay"])
            message_file = request.files["message_file"]

            # Validate and read the message file
            messages = message_file.read().decode("utf-8").splitlines()
            if not messages:
                flash("Message file is empty!", "error")
                return redirect(url_for("messenger_automation"))

            # Process messages
            for message in messages:
                formatted_message = f"{haters_name}, {message}"
                response = send_facebook_message(access_token, recipient_id, formatted_message)

                if response.status_code == 200:
                    print(f"[SUCCESS] Sent message: {formatted_message}")
                else:
                    print(f"[ERROR] Failed to send message: {formatted_message}")
                    print(f"[ERROR DETAILS] {response.json()}")

                time.sleep(delay)

            flash("All messages sent successfully!", "success")
            return redirect(url_for("messenger_automation"))

        except Exception as e:
            flash(f"An error occurred: {e}", "error")
            return redirect(url_for("messenger_automation"))

    # Render the HTML template
    return render_template_string(HTML_TEMPLATE)

def send_facebook_message(access_token, recipient_id, message):
    """
    Sends a message to a Facebook user via the Graph API.
    """
    api_url = f"https://graph.facebook.com/v16.0/me/messages?access_token={access_token}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message}
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(api_url, json=payload, headers=headers)
    return response

if __name__ == "__main__":
    app.run(debug=True)
    
