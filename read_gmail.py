import os.path
import base64
import time
from datetime import datetime  # For checking current time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate_gmail():
    """Authenticate the user with Gmail API and return the service object."""
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
    """Fetch unread emails."""
    results = service.users().messages().list(userId='me', labelIds=['UNREAD']).execute()
    return results.get('messages', [])

def generate_auto_reply(subject, sender):
    """Generate an auto-reply message."""
    reply = f"""
    Hi {sender},
    
    Thank you for reaching out regarding "{subject}". 
    I'm currently unavailable but will get back to you as soon as possible.
    
    Best regards,
    Auto Reply Bot
    """
    return reply.strip()

def send_reply(service, message_id, to_email, reply_subject, reply_text):
    """Send a reply to the given email."""
    message = MIMEText(reply_text)
    message['to'] = to_email
    message['subject'] = f"Re: {reply_subject}"
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().messages().send(
        userId='me',
        body={'raw': encoded_message, 'threadId': message_id}
    ).execute()

def mark_as_read(service, message_id):
    """Mark the email as read."""
    service.users().messages().modify(
        userId='me',
        id=message_id,
        body={'removeLabelIds': ['UNREAD']}
    ).execute()

def auto_reply():
    """Main function to handle auto-reply logic."""
    print("Running auto-reply...")
    service = authenticate_gmail()
    unread_msgs = get_unread_messages(service)

    if not unread_msgs:
        print("No unread messages.")
        return

    for msg in unread_msgs:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        headers = msg_data['payload']['headers']
        subject = next(header['value'] for header in headers if header['name'] == 'Subject')
        sender = next(header['value'] for header in headers if header['name'] == 'From')
        sender_email = sender.split("<")[-1].strip(">")

        print(f"Processing email from {sender} with subject: {subject}")
        reply_text = generate_auto_reply(subject, sender)
        send_reply(service, msg['id'], sender_email, subject, reply_text)
        mark_as_read(service, msg['id'])
        print(f"Replied to {sender} and marked the email as read.")

def main():
    """Run auto-reply only within a specific time range."""
    START_TIME = "00:00"  # Start time in HH:MM format
    END_TIME = "24:00"    # End time in HH:MM format

    while True:
        # Get the current time
        now = datetime.now().strftime("%H:%M")
        if START_TIME <= now <= END_TIME:  # Check if current time is within the time range
            print(f"Within active hours ({START_TIME} - {END_TIME}). Checking for unread emails...")
            auto_reply()
        else:
            print(f"Outside active hours ({START_TIME} - {END_TIME}). Waiting...")

        time.sleep(60)  # Check every minute

if __name__ == '__main__':
    main()
