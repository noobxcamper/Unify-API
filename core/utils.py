from rest_framework.response import Response
import json

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