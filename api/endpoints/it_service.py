import logging
from datetime import datetime

import requests
from django.template.loader import render_to_string
from rest_framework.response import Response
from rest_framework.views import APIView

from core.auth.permissions import AdminRole, ITRole
from core.config.obo_flow import get_app_token
from core.utils import create_audit_log

# Logging and auditing
audit_category = "IT Service"
logger = logging.getLogger(__name__)

class ITServiceMail(APIView):
    permission_classes = [ AdminRole | ITRole ]

    def post(self, request):
        first_name = request.data.get('first_name')
        recipient_email = request.data.get('to')
        login_email = request.data.get('loginEmail')
        password = request.data.get('password')
        start_date = datetime.strptime(request.data.get('startDate'), '%Y-%m-%d').strftime('%d/%m/%Y')
        headers = {"Authorization": f"Bearer {get_app_token()}", "Content-Type": "application/json"}

        html_content = render_to_string("mail/new_employee.html", {
            "first_name": first_name,
            "email": login_email,
            "password": password,
            "start_date": start_date
        })

        message = {
            "message": {
                "subject": "Welcome to Experior - Your Temporary Login Credentials",
                "body": {
                    "contentType": "HTML",
                    "content": html_content,
                },
                "toRecipients": [
                    { "emailAddress": { "address": recipient_email } },
                ]
            }
        }

        response = requests.post(f"https://graph.microsoft.com/v1.0/users/64dd9266-2157-4e78-97e8-068c691a0777/sendMail",
                                 headers=headers,
                                 json=message)

        create_audit_log(
            request,
            category = audit_category,
            action = "Mail Send",
            meta={
                'recipient': recipient_email,
            }
        )

        if response.status_code == 202:
            return Response(status=202)

        return Response(response.content, status=response.status_code)