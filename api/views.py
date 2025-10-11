import secrets
import string

import requests
from django.core.mail import EmailMessage, get_connection
from django.template.loader import render_to_string
from requests import post
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from core.models import EmailSettings, PurchaseOrders, ApprovalSettings
from core.msgraph import generate_obo_token
from core.permissions import AdminPermission, UserPermission
from core.utils import json_validator
from .serializers import PurchaseOrdersSerializer, ApprovalSettingsSerializer
from .zoho import get_valid_token


#region Files API
# @api_view(["GET"])
# @permission_classes([AdminPermission | FinancePermission])
# def get_download_url(request):
#     blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
#     blob_name = request.GET.get("filename")
#
#     blob_client = blob_service_client.get_blob_client(container=AZURE_STORAGE_CONTAINER, blob=blob_name)
#
#     # Generate a SAS token valid for 1 hour
#     sas_token = generate_blob_sas(
#         account_name=blob_service_client.account_name,
#         account_key=AZURE_STORAGE_CONNECTION_KEY,
#         container_name=AZURE_STORAGE_CONTAINER,
#         blob_name=blob_name,
#         permission=BlobSasPermissions(read=True),
#         expiry=datetime.now(timezone.utc) + timedelta(hours=1),
#     )
#
#     print(datetime.now(timezone.utc) + timedelta(hours=1))
#
#     download_url = f"{blob_service_client.url}{AZURE_STORAGE_CONTAINER}/{blob_name}?{sas_token}"
#     return Response({"download_url": download_url})

# @api_view(["GET"])
# @permission_classes([AdminPermission | FinancePermission])
# def get_upload_url(request):
#     blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
#     blob_name = request.GET.get("filename")
#
#     blob_client = blob_service_client.get_blob_client(container=AZURE_STORAGE_CONTAINER, blob=blob_name)
#
#     # Generate a SAS token valid for 1 hour
#     sas_token = generate_blob_sas(
#         account_name=blob_service_client.account_name,
#         account_key=AZURE_STORAGE_CONNECTION_KEY,
#         container_name=AZURE_STORAGE_CONTAINER,
#         blob_name=blob_name,
#         permission=BlobSasPermissions(write=True),
#         expiry=datetime.now(timezone.utc) + timedelta(hours=1),
#     )
#
#     print(datetime.now(timezone.utc) + timedelta(hours=1))
#
#     upload_url = f"{blob_service_client.url}{AZURE_STORAGE_CONTAINER}/{blob_name}?{sas_token}"
#     return Response({"upload_url": upload_url})
#endregion

@api_view(["GET"])
@permission_classes([AdminPermission | UserPermission])
def generate_password(request):
    password_requirement = string.ascii_letters + string.digits + string.punctuation
    password_length = 16
    password = "".join(secrets.choice(password_requirement) for _ in range(password_length))

    password_data = {
        "password": password
    }

    return Response(password_data)

@api_view(["POST"])
@permission_classes([AdminPermission | UserPermission])
def zoho_create_ticket(request):
    is_error, data_or_error_response = json_validator(request.body, required_fields=["ticket_subject", "ticket_body"])
    
    if is_error:
        return data_or_error_response
    
    json_data = data_or_error_response
    
    api_endpoint = "https://desk.zoho.com/api/v1/tickets"
    department_id = "1096658000000006907" # IT Helpdesk
    contact_id = "1096658000001801001" # Unify Application
    agent_id = "1096658000000139001" # Dylan
    ticket_subject = json_data.get("ticket_subject")
    ticket_body = json_data.get("ticket_body")
    ticket_classification = "Purchase Order (IT Only)"
    
    headers = {
        "Authorization": f"Zoho-oauthtoken {get_valid_token()}",
        "Content-Type": "application/json"
    }
    
    data = {
        "subject": ticket_subject,
        "description": ticket_body,
        "departmentId": department_id,
        "contactId": contact_id,
        # "assigneeId": agent_id,
        "classification": ticket_classification
    }
    
    zoho_api_response = post(url=api_endpoint, json=data, headers=headers)

    return Response(zoho_api_response.json())

@api_view(["POST"])
@permission_classes([AdminPermission | UserPermission])
def send_email(request):
    is_error, data_or_error_response = json_validator(request.body, required_fields=["subject", "to"])
    
    if is_error:
        return data_or_error_response
    
    json_data = data_or_error_response
    
    mail_config = EmailSettings.objects.first()
    html_content = render_to_string("mail/new_employee.html", {
        "first_name": "Hazem",
        "email": "h.abo-hashima@experiorheadoffice.ca",
        "password": "long_ass_password",
        "start_date": "01/01/1992"
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
        subject=json_data.get("subject"),
        body=html_content,
        from_email=mail_config.email_username,
        to=[json_data.get("to")],
        connection=connection
    )
    
    message.content_subtype = "html"
    message.send()
    
    return Response({"message": "email sent successfully"})

@api_view(["POST"])
@permission_classes([AdminPermission | UserPermission | HasAPIKey])
def send_new_employee_email(request):
    is_error, data_or_error_response = json_validator(request.body, required_fields=["to", "firstName", "loginEmail", "password", "startDate"])
    
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
    
    return Response({"message": "email sent successfully"})

@api_view(["GET"])
@permission_classes([AdminPermission | UserPermission])
def get_last_order(request):
    latest_order = PurchaseOrders.objects.last()
    response_data = {
        "order_number": latest_order.order_number
    }
    
    return Response(response_data, status=200)

class PurchaseOrdersView(APIView):
    permission_classes = [ HasAPIKey | AdminPermission | UserPermission ]
    
    def get(self, request, order_number=None):
        if order_number is None:
            orders = PurchaseOrders.objects.all()
            serializer = PurchaseOrdersSerializer(orders, many=True)
            
            return Response(serializer.data)
        
        try:
            order = PurchaseOrders.objects.get(order_number=order_number)
            serializer = PurchaseOrdersSerializer(order, data=request.data, partial=True)
            
            if serializer.is_valid():
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)
        except:
            error_response = {
                "error": [{
                    "error_code": "InvalidQuery",
                    "message": "could not find order with the order number specified"
                }]
            }
            return Response(error_response, status=400)
    
    def post(self, request):
        serializer = PurchaseOrdersSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
    
    def patch(self, request, order_number=None):
        if order_number is None:
            error_response = {
                "error": [{
                    "error_code": "InvalidQuery",
                    "message": "order number cannot be null or out of bounds"
                }]
            }
            return Response(error_response, status=400)
        
        
        order = PurchaseOrders.objects.get(order_number=order_number)
        serializer = PurchaseOrdersSerializer(order, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
    
    # def delete(self, request, order_id):
    #     order = PurchaseOrders.objects.get(submission_id=order_id)
    #     order.delete()

    #     return Response(status=204)

class ApprovalSettingsView(APIView):
    permission_classes = [ HasAPIKey | AdminPermission | UserPermission ]

    def get(self, request):
        approval_settings = ApprovalSettings.objects.first()
        serializer = ApprovalSettingsSerializer(approval_settings)

        return Response(serializer.data, status=200)

    def post(self, request):
        return None
    
    def patch(self, request):
        approval_settings = ApprovalSettings.objects.first()
        serializer = ApprovalSettingsSerializer(approval_settings, request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

class GraphUsersView(APIView):
    permission_classes = [ HasAPIKey | AdminPermission | UserPermission ]

    def get(self, request):
        obo_token = generate_obo_token(request.auth)

        # setup headers dict
        auth_header = {"Authorization": f"Bearer {obo_token}"}

        # perform graph request
        response = requests.get("https://graph.microsoft.com/v1.0/users", headers=auth_header)

        return Response(response.json())