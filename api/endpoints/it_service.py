from datetime import datetime

from django.core.mail import get_connection, EmailMessage
from django.template.loader import render_to_string
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import EmailSettings
from core.auth.permissions import AdminRole, ITRole
from core.utils import create_audit_log, TimeConverter

# Logging and auditing
audit_category = "IT Service"

class ITServiceMail(APIView):
    permission_classes = [ AdminRole | ITRole ]

    def post(self, request):
        html_content = render_to_string("mail/new_employee.html", {
            "first_name": request.data.get("firstName"),
            "email": request.data.get("loginEmail"),
            "password": request.data.get("password"),
            "start_date": datetime.strptime(request.data.get('startDate'), '%Y-%m-%d').strftime('%d/%m/%Y')
        })

        mail_config = EmailSettings.objects.first()

        # create smtp connection
        connection = get_connection(
            host=mail_config.email_host,
            port=mail_config.email_port,
            username=mail_config.email_username,
            password=mail_config.email_password,
            use_tls=mail_config.email_use_tls,
            fail_silently=False
        )

        message = EmailMessage(
            subject="Welcome to Experior - Your Temporary Login Credentials",
            body=html_content,
            from_email=mail_config.email_username,
            to=[request.data.get("to")],
            connection=connection
        )

        message.content_subtype = "html"
        message.send()

        create_audit_log(
            request,
            category = audit_category,
            action = "Mail Send",
            meta={
                'recipient': request.data.get('to'),
            }
        )

        return Response({"message": "email sent successfully"})