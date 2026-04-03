from requests import post
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from core.config.zoho_config import ZohoConfig
from core.auth.permissions import AdminRole
from core.utils import json_validator

class ZohoTicketView(APIView):
    permission_classes = [ AdminRole | HasAPIKey ]

    def post(self, request):
        is_error, data_or_error_response = json_validator(request.body,
                                                          required_fields=["ticket_subject", "ticket_body"])

        if is_error:
            return data_or_error_response

        json_data = data_or_error_response

        zoho_token = ZohoConfig()

        api_endpoint = "https://desk.zoho.com/api/v1/tickets"
        department_id = "1096658000000006907"  # IT Helpdesk
        contact_id = "1096658000001801001"  # Unify Application
        agent_id = "1096658000000139001"  # Dylan
        ticket_subject = json_data.get("ticket_subject")
        ticket_body = json_data.get("ticket_body")
        ticket_classification = "Purchase Order (IT Only)"

        headers = {
            "Authorization": f"Zoho-oauthtoken {zoho_token.get_valid_token()}",
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