import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd

def load_participant_data(file_path):
    """
    Reads participant details from an Excel file.
    Expected columns: Speaker_Label, Name, Email
    Returns a dictionary mapping Speaker_Label to a dict with Name and Email.
    """
    try:
        df = pd.read_excel(file_path)
        participant_dict = {}
        for index, row in df.iterrows():
            speaker_label = str(row['Speaker_Label']).strip()
            participant_dict[speaker_label] = {
                'Name': str(row['Name']).strip(),
                'Email': str(row['Email']).strip()
            }
        return participant_dict
    except Exception as e:
        print(f"Error loading participant data from {file_path}: {e}")
        return {}

def dispatch_meeting_notes(summary, action_items, participant_dict):
    """
    Sends personalized formatted HTML emails to participants.
    """
    smtp_email = os.getenv('SMTP_EMAIL')
    smtp_password = os.getenv('SMTP_PASSWORD')
    
    if not smtp_email or not smtp_password:
        print("SMTP Credentials not found in environment variables (SMTP_EMAIL, SMTP_PASSWORD).")
        print("Skipping actual email dispatch for testing.")
        
    # Group action items by assignee
    # action_items shape: [{"task": "Design DB", "assignee": "Speaker A", "deadline": "Monday"}]
    assigned_tasks = {}
    for item in action_items:
        assignee = item.get("assignee")
        if assignee not in assigned_tasks:
            assigned_tasks[assignee] = []
        assigned_tasks[assignee].append(item)
        
    for label, details in participant_dict.items():
        name = details.get("Name")
        email_address = details.get("Email")
        
        if not email_address or email_address.lower() == 'nan':
            print(f"Skipping dispatch for {label} - Invalid email: {email_address}")
            continue
            
        tasks = assigned_tasks.get(label, [])
        
        # Build HTML Email
        html_content = build_html_email(name, summary, tasks)
        
        msg = MIMEMultipart("alternative")
        msg['Subject'] = "Meeting Notes & Action Items"
        msg['From'] = smtp_email if smtp_email else "Meeting Assistant <bot@example.com>"
        msg['To'] = email_address
        
        part = MIMEText(html_content, 'html')
        msg.attach(part)
        
        print(f"Prepared email for {name} ({email_address}) with {len(tasks)} tasks.")
        
        if smtp_email and smtp_password:
            try:
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(smtp_email, smtp_password)
                    server.send_message(msg)
                print(f"Email successfully sent to {email_address}!")
            except Exception as e:
                print(f"Failed to send email to {email_address}: {e}")
        else:
            print(f"Simulated sending to {email_address}:\n{html_content[:200]}...\n")

def build_html_email(name, summary, tasks):
    """
    Builds the personalized HTML content.
    """
    tasks_html = ""
    if tasks:
        tasks_html = "<h3>Your Action Items:</h3><ul>"
        for task in tasks:
            task_desc = task.get('task', 'Unknown task')
            deadline = task.get('deadline', 'No deadline')
            tasks_html += f"<li><strong>{task_desc}</strong> (Deadline: {deadline})</li>"
        tasks_html += "</ul>"
    else:
        tasks_html = "<p><em>You have no action items assigned from this meeting.</em></p>"

    html = f"""
    <html>
      <head>
        <style>
          body {{ font-family: Arial, sans-serif; color: #333; line-height: 1.6; }}
          .container {{ width: 80%; margin: 20px auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }}
          .header {{ background-color: #f4f4f4; padding: 10px 20px; border-radius: 8px 8px 0 0; border-bottom: 2px solid #0056b3; }}
          .content {{ padding: 20px; }}
          .footer {{ margin-top: 20px; font-size: 0.9em; color: #777; text-align: center; }}
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <h2>Meeting Notes & Action Items</h2>
          </div>
          <div class="content">
            <p>Hi {name},</p>
            <p>Here is the summary of our recent meeting:</p>
            <div style="background-color: #fcfcfc; padding: 15px; border-left: 4px solid #0056b3; margin-bottom: 20px;">
              {summary}
            </div>
            {tasks_html}
            <p>Best regards,<br>Multi-Modal Meeting Assistant</p>
          </div>
          <div class="footer">
            <p>This is an automated message. Please do not reply directly to this email.</p>
          </div>
        </div>
      </body>
    </html>
    """
    return html
