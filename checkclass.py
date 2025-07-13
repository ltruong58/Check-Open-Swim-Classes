import requests
import json
import smtplib
from email.mime.text import MIMEText
import os

def checkAvailableClass (url, payload):
    hasChanged = False

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        result_data = response.json()
        activities = result_data['body']['activity_items']

        print("API call successful.")

        open_classes = []

        for item in activities:
            if(item.get('urgent_message').get('status_description') != 'Full'):
                hasChanged = True
                open_classes.append(str(item.get('number') + " " + item.get('name')))
            print(item.get('number'), item.get('urgent_message').get('status_description'))
        return hasChanged, open_classes

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the API call: {e}")

def sendEmail(classList):
    # To run on Server
    sender_email = os.environ['EMAIL_USER']
    sender_password = os.environ['EMAIL_PASS']
    recipient_email = os.environ['TO_EMAIL']

    # To run on local
    # sender_email = 'long.truongnguyenthanh@gmail.com'
    # sender_password = 'amfn dzds mbns xjtf'
    # recipient_email = 'long.truongswe@gmail.com'

    subject = "GitHub Action: Open classes"
    body = "New open class(es) are now available: \n" + " \n".join(item for item in classList)

    print(body)
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")


api_url = "https://anc.apm.activecommunities.com/buenapark/rest/activities/list?locale=en-US"  # Replace with your API endpoint
payload = {
  "activity_search_pattern": {
    "skills": [],
    "time_after_str": "",
    "days_of_week": 'null',
    "activity_select_param": 2,
    "center_ids": [],
    "time_before_str": "",
    "open_spots": 'null',
    "activity_id": 'null',
    "activity_category_ids": [],
    "date_before": "",
    "min_age": 'null',
    "date_after": "",
    "activity_type_ids": [],
    "site_ids": [],
    "for_map": 'false',
    "geographic_area_ids": [],
    "season_ids": [],
    "activity_department_ids": [],
    "activity_other_category_ids": [],
    "child_season_ids": [],
    "activity_keyword": "starfish",
    "instructor_ids": [],
    "max_age": 'null',
    "custom_price_from": "",
    "custom_price_to": ""
  },
  "activity_transfer_pattern": {}
}

isAvailable, classList = checkAvailableClass (api_url, payload)

if isAvailable:
    sendEmail(classList)
    