import logging
from datetime import datetime

import requests
import time
from django.core.cache import cache
from django.template.loader import render_to_string
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

from core.auth.permissions import AdminRole, HrRole, ITRole
from core.config.obo_flow import get_obo_token, get_app_token
from core.utils import generate_password, create_audit_log

# Logging and auditing
audit_category = "Graph"
logger = logging.getLogger(__name__)

class User(APIView):
    permission_classes = [ AdminRole | HrRole | ITRole ]

    def get(self, request, user_id):
        app_token = get_app_token()
        headers = {"Authorization": f"Bearer {app_token}"}

        response = requests.get(f"https://graph.microsoft.com/v1.0/users/{user_id}", headers=headers)

        return Response(response.json())

class OwnedDevices(APIView):
    permission_classes = [ AdminRole | HrRole | ITRole ]

    def get(self, request, user_id):
        obo_token = get_obo_token(request.user.oid, request.auth)
        headers = {"Authorization": f"Bearer {obo_token}"}

        response = requests.get(f"https://graph.microsoft.com/v1.0/users/{user_id}/ownedDevices", headers=headers)

        return Response(response.json())

class GroupMembers(APIView):
    permission_classes = [ AdminRole | HrRole | ITRole ]

    def get(self, request, group_id):
        start = time.perf_counter()

        app_token = get_app_token()
        cache_ttl = (60 * 15)
        cache_key = f"graph_group_members:{group_id}"
        headers = {"Authorization": f"Bearer {app_token}"}

        # retrieve the cached data if available or bypass if requested
        if not request.query_params.get('cache_bust') == '1':
            cached_data = cache.get(cache_key)
            if cached_data:
                end = time.perf_counter()
                total_time = end - start

                print(f"Execution time: {total_time:.2f} seconds")

                return Response(cached_data)

        print('bypassed cache')
        url = f"https://graph.microsoft.com/v1.0/groups/{group_id}/members"
        raw_data = []

        while url:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                return Response(
                    {"error": "Failed to fetch data from Microsoft Graph", "details": response.text},
                    status=response.status_code
                )

            data = response.json()
            raw_data.extend(data.get("value", []))
            url = data.get("@odata.nextLink")  # Continue pagination if available

        # cache the response
        cache.set(cache_key, raw_data, timeout=cache_ttl)

        end = time.perf_counter()
        total_time = end - start

        print(f"Execution time: {total_time:.2f} seconds")

        return Response(raw_data)

class OffboardUser(APIView):
    permission_classes = [ AdminRole | HrRole | ITRole | HasAPIKey ]

    def __delete_auth_methods(self, obo_token, user_id):
        """
        Delete all authentication methods associated with this user. This will force a re-registration

        https://learn.microsoft.com/en-us/graph/api/resources/authenticationmethods-overview?view=graph-rest-beta#require-re-register-multifactor-authentication

        Parameters:
            obo_token: the OBO token for the user
            user_id: the user id

        Returns:
            the response for the LAST DELETE request
        """
        # define all auth endpoints for deletion (thanks Microsoft!)
        auth_delete_endpoints = {
            '#microsoft.graph.emailAuthenticationMethod':
                "emailMethods/{id}",

            '#microsoft.graph.externalAuthenticationMethod':
                "externalAuthenticationMethods/{id}/$ref",

            '#microsoft.graph.fido2AuthenticationMethod':
                "fido2Methods/{id}",

            '#microsoft.graph.hardwareOathAuthenticationMethod':
                "hardwareOathMethods/{id}",

            '#microsoft.graph.microsoftAuthenticatorAuthenticationMethod':
                "microsoftAuthenticatorMethods/{id}",

            '#microsoft.graph.phoneAuthenticationMethod':
                "phoneMethods/{id}",

            '#microsoft.graph.platformCredentialAuthenticationMethod':
                "platformCredentialMethods/{id}",

            '#microsoft.graph.softwareOathAuthenticationMethod':
                "softwareOathMethods/{id}",

            '#microsoft.graph.temporaryAccessPassAuthenticationMethod':
                "temporaryAccessPassMethods/{id}",

            '#microsoft.graph.windowsHelloForBusinessAuthenticationMethod':
                "windowsHelloForBusinessMethods/{id}",

            '#microsoft.graph.qrCodePinAuthenticationMethod':
                "qrCodePinMethod",
        }

        base_url = f"https://graph.microsoft.com/beta/users/{user_id}/authentication"
        headers = {"Authorization": f"Bearer {obo_token}"}

        response = requests.get(f"{base_url}/methods", headers=headers)
        response.raise_for_status()

        for auth_method in response.json().get('value', []):
            auth_type = auth_method['@odata.type']
            auth_id = auth_method['id']
            endpoint = auth_delete_endpoints.get(auth_type)

            # skip password authentication, this cannot be deleted
            if auth_type == '#microsoft.graph.passwordAuthenticationMethod':
                continue

            if endpoint is None:
                print(f"Unknown auth type: {auth_type}")
                continue

            # If endpoint template contains {id}, substitute it, otherwise treat as singleton
            if "{id}" in endpoint:
                path = endpoint.format(id=auth_id)
                url = f"{base_url}/{path}"
            else:
                url = f"{base_url}/{endpoint}"

            requests.delete(url, headers=headers)

        return Response(status=204)

    def post(self, request, user_id):
        app_token = get_app_token()
        headers = {"Authorization": f"Bearer {app_token}", "Content-Type": "application/json"}

        # craft the json data
        account_reset_data = {
            "accountEnabled": "false",
            "passwordProfile": {
                "forceChangePasswordNextSignIn": "true",
                "forceChangePasswordNextSignInWithMfa": "false",
                "password": generate_password()
            }
        }

        # delete auth methods
        self.__delete_auth_methods(app_token, user_id)

        # revoke sign-in sessions
        requests.post(f"https://graph.microsoft.com/v1.0/users/{user_id}/revokeSignInSessions", headers=headers)

        # disable account and reset password
        response = requests.patch(f"https://graph.microsoft.com/v1.0/users/{user_id}", json=account_reset_data, headers=headers)

        if response.status_code == 204:
            create_audit_log(
                request,
                category=audit_category,
                action="Offboarded User",
                meta={
                    'user': user_id,
                }
            )
            return Response({"status": "success"}, status=200)

        return Response(response.json(), status=response.status_code)

class RemoveUserLicenses(APIView):
    permission_classes = [ AdminRole | HrRole | ITRole ]

    def post(self, request):
        pass

class SendMail(APIView):
    permission_classes = [ AdminRole | ITRole ]

    def post(self, request):
        first_name = request.data.get('first_name')
        recipient_email = request.data.get('to')
        login_email = request.data.get('loginEmail')
        password = request.data.get('password')
        start_date = datetime.strptime(request.data.get('startDate'), '%Y-%m-%d').strftime('%d/%m/%Y')
        headers = {"Authorization": f"Bearer {get_app_token()}", "Content-Type": "application/json"}

        print(request.data.get('first_name'))

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