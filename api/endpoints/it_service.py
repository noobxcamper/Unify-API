from django.core.mail import get_connection, EmailMessage
from django.template.loader import render_to_string
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from api.models import EmailSettings
from core.auth.permissions import AdminRole, ITRole
from core.models import AuditLog
from core.utils import json_validator

# Logging and auditing
audit_category = "ITService"

class ITServiceMail(APIView):
    permission_classes = [ AdminRole | ITRole ]

    def post(self, request):
        is_error, data_or_error_response = json_validator(request.body,
                                                          required_fields=["to", "firstName", "loginEmail", "password",
                                                                           "startDate"])

        if is_error:
            return data_or_error_response

        json_data = data_or_error_response

        mail_config = EmailSettings.objects.first()
        html_content = render_to_string("mail/new_employee.html", {
            "first_name": json_data.get("firstName"),
            "email": json_data.get("loginEmail"),
            "password": json_data.get("password"),
            "start_date": json_data.get("startDate")
        })

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
            to=[json_data.get("to")],
            connection=connection
        )

        message.content_subtype = "html"
        message.send()

        AuditLog.objects.create(
            oid = request.user.oid,
            name = request.user.name,
            email = request.user.email,
            category = audit_category,
            action = "Mail send to recipient",
            additional_details = f"Recipient: {json_data.get('to')}"
        )

        return Response({"message": "email sent successfully"})