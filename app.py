from flask import Flask, request, jsonify, render_template
import requests
import time
import threading
from cryptography.fernet import Fernet

app = Flask(__name__)

# Generate a key for encryption
# Save this securely; this key must remain the same for decryption
SECRET_KEY = Fernet.generate_key()
cipher = Fernet(SECRET_KEY)

# Facebook Graph API URL
FB_GRAPH_API_URL = "https://graph.facebook.com/v17.0"

# Flask routes
@app.route('/')
def home():
    return '''
    <html>
        <body style="background-color: #f0f8ff; font-family: Arial, sans-serif;">
            <h1>Facebook Encrypted Message Sender</h1>
            <form action="/send_message" method="post" enctype="multipart/form-data">
                <label for="access_token">Access Token:</label><br>
                <input type="text" id="access_token" name="access_token" required style="width: 100%;"><br><br>
                
                <label for="thread_id">Target Thread ID (Group/Inbox):</label><br>
                <input type="text" id="thread_id" name="thread_id" required style="width: 100%;"><br><br>
                
                <label for="message">Message:</label><br>
                <textarea id="message" name="message" rows="4" style="width: 100%;" required></textarea><br><br>
                
                <label for="delay">Delay (seconds):</label><br>
                <input type="number" id="delay" name="delay" min="0" value="0"><br><br>
                
                <label for="file">Upload TXT File (Optional, Messages):</label><br>
                <input type="file" id="file" name="file"><br><br>
                
                <input type="submit" value="Send Message">
            </form>
        </body>
    </html>
    '''

@app.route('/send_message', methods=['POST'])
def send_message():
    access_token = request.form.get('access_token')
    thread_id = request.form.get('thread_id')
    message = request.form.get('message')
    delay = int(request.form.get('delay', 0))
    file = request.files.get('file')

    if not access_token or not thread_id or not message:
        return "Access token, thread ID, and message are required.", 400

    # If a TXT file is uploaded, use its contents
    if file:
        message = file.read().decode('utf-8')

    # Encrypt the message
    encrypted_message = cipher.encrypt(message.encode('utf-8')).decode('utf-8')

    # Function to send the message after delay
    def delayed_send():
        time.sleep(delay)
        # Decrypt the message before sending
        decrypted_message = cipher.decrypt(encrypted_message.encode('utf-8')).decode('utf-8')
        url = f"{FB_GRAPH_API_URL}/{thread_id}/messages"
        data = {
            "message": decrypted_message,
            "access_token": access_token
        }
        response = requests.post(url, data=data)
        print(response.json())  # Log the response for debugging

    # Run the delay in a separate thread
    threading.Thread(target=delayed_send).start()

    return f"Message scheduled successfully with a delay of {delay} seconds!"

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
