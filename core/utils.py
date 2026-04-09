from rest_framework.response import Response
import json, string, secrets, random
from datetime import datetime, timezone

from core.models import AuditLog

class TimeConverter:
    def to_utc(self, time):
        return datetime.fromisoformat(time)

    def from_utc(self, time):
        return datetime.fromisoformat(time).astimezone().strftime('%d/%m/%Y')

    def from_utc_with_tz(self, time):
        return datetime.fromisoformat(time).astimezone().strftime('%d/%m/%Y %H:%M:%S')

def json_validator(data, required_fields=None):
    """
    Validates JSON data and required fields
    
    Parameters:
        data (json): the JSON data to be validated.
        required_fields ([str]): an array of fields to check for.
        
    Returns:
        JSON data, or a Rest Framework Response error.
    """
    try:
        json_data = json.loads(data)
        
        missing_fields = [field for field in required_fields if field not in json_data]
        
        if missing_fields:
            error_response = {
                "error": [{
                    "errorCode": "0x000001",
                    "message": "Required fields are missing",
                    "missingFields": missing_fields
                }]
            }
            return True, Response(error_response, status=400)
        else:
            return False, json_data
        
    except json.JSONDecodeError:
        error_response = {
            "error": [{
                "errorCode": "0x000002",
                "message": "Unable to decode json data, make sure you are sending json data in the body"
            }]
        }
        return True, Response(error_response, status=400)

def generate_password(pass_length=12):
    if pass_length < 4:
        raise ValueError("Password length must be at least 4")

    # Required character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation

    password = [
        secrets.choice(lowercase),
        secrets.choice(uppercase),
        secrets.choice(digits),
        secrets.choice(symbols)
    ]

    # Fill the rest
    all_chars = lowercase + uppercase + digits + symbols
    password += [secrets.choice(all_chars) for _ in range(pass_length - 4)]

    # Shuffle to avoid predictable pattern
    random.SystemRandom().shuffle(password)

    return "".join(password)

def create_audit_log(request, category, action, meta):
    if request.is_api_key:
        AuditLog.objects.create(
            request_id=request.request_id,
            remote_ip=request.remote_ip,
            user_agent=request.user_agent,
            category=category,
            action=action,
            api_key_used=request.is_api_key,
            user_details={
                'key_name': request.api_key.name,
                'key_prefix': request.api_key.prefix,
            },
            meta=meta
        )
    else:
        AuditLog.objects.create(
            request_id=request.request_id,
            remote_ip=request.remote_ip,
            user_agent=request.user_agent,
            category=category,
            action=action,
            user_details={
                'oid': request.user.oid,
                'name': request.user.name,
                'email': request.user.email,
            },
            meta=meta
        )