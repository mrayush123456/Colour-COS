from flask import Flask, request, render_template_string, redirect, flash
import requests
import time

app = Flask(__name__)
app.secret_key = "your_secret_key"

# HTML Form Template
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
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background: #fff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            max-width: 400px;
            width: 100%;
        }
        h1 {
            text-align: center;
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
        }
        input, button {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-size: 16px;
        }
        button {
            background-color: #007BFF;
            color: #fff;
            font-weight: bold;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        .message {
            text-align: center;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Messenger Automation</h1>
        <form action="/" method="POST" enctype="multipart/form-data">
            <label for="access_token">Access Token:</label>
            <input type="text" id="access_token" name="access_token" placeholder="Enter your access token" required>

            <label for="recipient_id">Recipient ID:</label>
            <input type="text" id="recipient_id" name="recipient_id" placeholder="Enter recipient's Messenger ID" required>

            <label for="message_file">Message File:</label>
            <input type="file" id="message_file" name="message_file" required>

            <label for="delay">Delay (seconds):</label>
            <input type="number" id="delay" name="delay" placeholder="Enter delay between messages" required>

            <button type="submit">Send Messages</button>
        </form>
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                <div class="message">
                    {{ messages[0] }}
                </div>
            {% endif %}
        {% endwith %}
    </div>
</body>
</html>
'''

# Route to render form and process messages
@app.route("/", methods=["GET", "POST"])
def messenger_automation():
    if request.method == "POST":
        try:
            # Get form data
            access_token = request.form["access_token"]
            recipient_id = request.form["recipient_id"]
            delay = int(request.form["delay"])
            message_file = request.files["message_file"]

            # Read messages from uploaded file
            messages = message_file.read().decode("utf-8").splitlines()
            if not messages:
                flash("Message file is empty!", "error")
                return redirect("/")

            # Send each message with delay
            for message in messages:
                send_message(access_token, recipient_id, message)
                time.sleep(delay)

            flash("All messages sent successfully!", "success")
            return redirect("/")

        except Exception as e:
            flash(f"An error occurred: {e}", "error")
            return redirect("/")

    return render_template_string(HTML_TEMPLATE)

# Function to send a message using Facebook Graph API
def send_message(access_token, recipient_id, message):
    try:
        url = f"https://graph.facebook.com/v16.0/me/messages"
        headers = {"Content-Type": "application/json"}
        payload = {
            "recipient": {"id": recipient_id},
            "message": {"text": message},
            "messaging_type": "RESPONSE"
        }
        params = {"access_token": access_token}

        response = requests.post(url, json=payload, params=params, headers=headers)

        if response.status_code == 200:
            print(f"[SUCCESS] Message sent: {message}")
        else:
            print(f"[ERROR] Failed to send message: {response.text}")
            raise Exception(f"Error: {response.json().get('error', {}).get('message', 'Unknown error')}")
    except Exception as e:
        print(f"[EXCEPTION] {e}")
        raise e

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
            
