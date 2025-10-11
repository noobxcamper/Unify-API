from datetime import timedelta
from django.utils import timezone
from msal import ConfidentialClientApplication
from backend.settings import AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID
import jwt

def generate_obo_token(user_access_token):
    app = ConfidentialClientApplication(
        client_id=AZURE_CLIENT_ID,
        client_credential=AZURE_CLIENT_SECRET,
        authority=f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
    )

    result = app.acquire_token_on_behalf_of(
        user_assertion=user_access_token,
        scopes=["https://graph.microsoft.com/.default"]
    )

    access_token = result["access_token"]
    expires_in = result["expires_in"]
    expires_at = timezone.now() + timedelta(seconds=expires_in)

    # get oid from claims
    claims = jwt.decode(access_token, options={"verify_signature": False})
    oid = claims.get("oid")

    return access_token