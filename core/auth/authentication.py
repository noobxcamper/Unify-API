from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from jwt.algorithms import RSAAlgorithm
from service.settings import AZURE_TENANT_ID, AZURE_CLIENT_ID
from django.core.cache import cache
from core.models import AppUser
import jwt, requests, logging

KEYS_URL = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/discovery/v2.0/keys"
logger = logging.getLogger(__name__)

class TokenVerification:
    """
    Retrieves and caches Microsoft Entra public signing keys in Redis for 1 hour.
    Uses them to verify JWT signatures and claims.
    """

    audience_candidates = [
        AZURE_CLIENT_ID,
        "https://graph.microsoft.com",
    ]

    issuer_candidates = [
        f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/v2.0",
        f"https://sts.windows.net/{AZURE_TENANT_ID}/"
    ]

    def __get_cached_entra_key(self):
        cache_key = "entra_public_jwks"
        ttl = 3600          # seconds
        request_timeout = 5 # seconds

        cached_keys = cache.get(cache_key)
        if cached_keys:
            logger.info("Found cached JWKS key, returning the cached key")
            return cached_keys

        try:
            response = requests.get(KEYS_URL, timeout=request_timeout)
            response.raise_for_status()
            keys = response.json().get("keys", [])
            cache.set(cache_key, keys, timeout=ttl)
            logger.info(f"Retrieved and cached Microsoft Entra public JWKs from {KEYS_URL}")
            return keys
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to retrieve public verification key from {KEYS_URL}: {e}")
            raise AuthenticationFailed(f"Unable to retrieve public verification key from {KEYS_URL}")

    def verify_token(self, token):
        """
        Verifies a JWT against Microsoft Entra (Azure AD) signing keys.
        """
        try:
            unverified_header = jwt.get_unverified_header(token)
            kid = unverified_header.get("kid")
            if not kid:
                raise AuthenticationFailed("Token header is missing 'kid'")

            verification_keys = self.__get_cached_entra_key()
            rsa_key = None

            for key in verification_keys:
                if key["kid"] == kid:
                    rsa_key = RSAAlgorithm.from_jwk(key)
                    break

            if not rsa_key:
                logger.error("No matching key found for token signature verification")
                raise AuthenticationFailed("No matching key found for token signature verification")

            decoded_token = jwt.decode(
                token,
                rsa_key,
                algorithms=["RS256"],
                audience=self.audience_candidates,
                options={"verify_iss": False}
            )

            iss = decoded_token.get("iss")
            if iss not in self.issuer_candidates:
                raise AuthenticationFailed(f"Invalid issuer: {iss}")

            return decoded_token

        except jwt.ExpiredSignatureError as e:
            logger.warning(f"Invalid token: {str(e)}")
            raise AuthenticationFailed("Token has expired")

        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid token: {str(e)}")
            raise AuthenticationFailed(f"Invalid token: {str(e)}")

class EntraUser:
    def __init__(self, token_claims: dict):
        self.token_claims = token_claims or {}
        self.is_authenticated = True
        self.is_anonymous = False
        self.roles = token_claims.get("roles", [])
        self.oid = token_claims.get("oid")
        self.name = token_claims.get("name")
        self.email = token_claims.get("preferred_username")     # email address
        self.is_entra_authenticated = None

    def get(self, key, default=None):
        return self.token_claims.get(key, default)

class AzureADAuthentication(BaseAuthentication):
    """
    Extends the django rest framework authentication class to handle Azure AD authentication.
    """

    def authenticate(self, request):
        """
        Authenticates the user against the Azure AD tenant specified by the tenant ID.

        Returns:
            EntraUser and token tuple
        """
        token_verification = TokenVerification()
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1].strip()
        if not token:
            raise AuthenticationFailed("Token is missing 'Authorization'")

        verified_token = token_verification.verify_token(token)
        if not verified_token:
            raise AuthenticationFailed("Invalid token")

        aud_claim = verified_token.get("aud")
        if not aud_claim or aud_claim != AZURE_CLIENT_ID:
            raise AuthenticationFailed("Invalid audience claim")

        # Create a new EntraUser object and set the request.user
        request.user = EntraUser(verified_token)

        # Insert new entry into the DB for roles/permissions if the user does not
        # already exist
        AppUser.objects.get_or_create(
            oid=request.user.oid,
            name=request.user.name,
            email=request.user.email,
        )

        # Mark the user as authenticated for permissions
        request.user.is_entra_authenticated = True

        return request.user, token