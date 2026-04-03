import jwt
import logging
import time

from django.core.cache import cache
from msal import ConfidentialClientApplication
from rest_framework.exceptions import AuthenticationFailed

from service.settings import AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID

logger = logging.getLogger(__name__)

def get_obo_token(user_id, user_access_token):
    """
    Retrieve the OBO token from the cache, or generates a new one if the cached key does not exist or is expired.

    This token is used with Microsoft Graph only.

    Parameters:
        user_id (str): the oid from the user claims, usually request.user.oid
        user_access_token (str): the access token provided by the user

    Returns:
        The OBO token
    """

    cache_key = f"graph_obo_token:{user_id}"
    token = cache.get(cache_key)
    if token:
        return token

    app = ConfidentialClientApplication(
        client_id=AZURE_CLIENT_ID,
        client_credential=AZURE_CLIENT_SECRET,
        authority=f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
    )

    res = app.acquire_token_on_behalf_of(
        user_assertion=user_access_token,
        scopes=["https://graph.microsoft.com/.default"]
    )
    if "access_token" not in res:
        raise AuthenticationFailed(res.get("error_description") or "Failed OBO")

    token = res["access_token"]
    claims = jwt.decode(token, options={"verify_signature": False})
    ttl = max(0, int(claims["exp"] - time.time()) - 30)
    cache.set(cache_key, token, timeout=ttl)

    logger.info("Generated OBO token and stored in the cache")
    return token

def get_app_token():
    """
    Retrieve the app token from the cache, or generates a new one if the cached key does not exist or is expired.

    This token is used with Microsoft Graph only.

    Returns:
        The app token
    """

    cache_key = "app_token"
    token = cache.get(cache_key)
    if token:
        return token

    app = ConfidentialClientApplication(
        client_id=AZURE_CLIENT_ID,
        client_credential=AZURE_CLIENT_SECRET,
        authority=f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
    )

    res = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if "access_token" not in res:
        raise AuthenticationFailed(res.get("error_description") or "Failed to acquire app token")

    access_token = res["access_token"]

    # Decode to compute TTL
    claims = jwt.decode(access_token, options={"verify_signature": False})
    ttl = max(0, int(claims["exp"] - time.time()) - 30)  # subtract 30s for safety

    logger.info("Generated app token and stored in the cache")
    cache.set(cache_key, access_token, timeout=ttl)

    return access_token