import requests
from fastapi import HTTPException
from pydantic import EmailStr

from setting import settings

SENDGRID_EMAIL_FROM = settings.SENDGRID_EMAIL_FROM
SENDGRID_NAME_FROM = settings.SENDGRID_NAME_FROM
SENDGRID_HOST = settings.SENDGRID_HOST
SENDGRID_API_KEY = settings.SENDGRID_API_KEY
headers = {
  'Content-Type': 'application/json',
  'Authorization': f'Bearer {SENDGRID_API_KEY}',
}

# For feature custom multiple personalizations in the feature (Ex: send email to 2 recipients at 2 different times)
# def get_personalization(email_to: list[EmailStr], dynamic_template_data: dict) -> dict:
#   to = []
#   for e in email_to:
#     to.append({'email': e})
#   return {
#     'to': to,
#     'dynamic_template_data': dynamic_template_data
#   }

# Currently, BE not support multiple personalizations 
def get_payload(email_to: list[EmailStr], template_id: str, data: dict):
  to = []
  for e in email_to:
    to.append({'email': e})
  return {
    'from': {'email': SENDGRID_EMAIL_FROM, 'name': SENDGRID_NAME_FROM},
    'template_id': template_id,
    'personalizations': [{'to': to, 'dynamic_template_data': data}]
  }

def send_email(payload):
  response = requests.post(f'{SENDGRID_HOST}/mail/send', json=payload, headers=headers)
  if not str(response.status_code).startswith('20'):
    raise HTTPException(status_code=response.status_code, detail=response.json())
