import os.path
import base64
import openai
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import json

# Scopes for Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# Set your OpenAI API key here
openai.api_key = ''

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def get_unread_messages(service):
    results = service.users().messages().list(userId='me', labelIds=['UNREAD']).execute()
    return results.get('messages', [])

def generate_reply_with_chatgpt(subject, sender, body):
    # Send prompt to ChatGPT to generate a response
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"You received an email from {sender} with the subject '{subject}'. The message says:\n\n{body}\n\nPlease reply politely and professionally.",
        max_tokens=150
    )
    return response['choices'][0]['text'].strip()

def send_reply(service, message_id, reply_text):
    # Prepare reply message
    message = MIMEText(reply_text)
    message['to'] = 'recipient@example.com'
    message['subject'] = "Re: " + subject
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    # Send the reply
    send_result = service.users().messages().send(
        userId='me',
        body={'raw': encoded_message, 'threadId': message_id}
    ).execute()

def main():
    # Authenticate and initialize the API client
    service = authenticate_gmail()

    # Fetch unread messages
    unread_msgs = get_unread_messages(service)
    if not unread_msgs:
        print("No unread messages.")
        return

    for msg in unread_msgs:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        
        # Extract email details
        headers = msg_data['payload']['headers']
        subject = next(header['value'] for header in headers if header['name'] == 'Subject')
        sender = next(header['value'] for header in headers if header['name'] == 'From')
        if 'parts' in msg_data['payload']:
            body = base64.urlsafe_b64decode(msg_data['payload']['parts'][0]['body']['data']).decode('utf-8')
        else:
            body = "Could not fetch body content."

        # Generate reply with ChatGPT
        reply_text = generate_reply_with_chatgpt(subject, sender, body)
        print(f"Reply to {sender}:\n{reply_text}\n{'-'*50}")

        # Send the reply
        send_reply(service, msg['id'], reply_text)

        # Mark as read
        service.users().messages().modify(userId='me', id=msg['id'], body={'removeLabelIds': ['UNREAD']}).execute()

if __name__ == '__main__':
    main()
