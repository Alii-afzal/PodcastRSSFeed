def log_format(request, response, exception=None):
    user_id = request.user.id if request.user.is_authenticated else None
    user_info ={
        'user_id':user_id,
        'user_email': request.user.email if request.user.is_authenticated else ' ',
    }
    remote_host = request.META.get("REMOTE_ADDR",'-')
    request_line = request.method
    
    status_code = response.status_code if not exception else 500

    response_size = response.get('Content-Length', ' ') if response else ""
    print(response_size)
    referrer = request.META.get('HTTP_REFERRER', '-')
    elapsed_time = response.elapsed.total_seconds() if hasattr(response, 'elapsed') else None
    user_agent = request.headers.get('user-agen')
    event = f"{request.get_full_path()} HTTP/1.1"

    message = str(exception) if exception else 'Request is successfully'
    
    return {
        'user_info': user_info,
        'remote_host': remote_host,
        'request_line': request_line,
        'status_code': status_code,
        'response_size': response_size,
        'referrer': referrer,
        'elapsed_time': elapsed_time,
        'message': message,
        'user_agent': user_agent,
        'event': event,
    }

def authentication_logs_format(user, body, exception=None):
    message = str(exception) if exception else 'Consume is seccssfully'
    
    return {
        'user_id': str(user.id ),
        'user_phone': str(user.phone),
        'user_agent': body["user_agent"],
        'event': f"consumer.{body['routing_key']}",
        "status": "success",
        'message': message
    }
    
def rss_log_format(body, exception=None):

    message = str(exception) if exception else 'Consume is successfully'

    return {
        'event': f"consumer.{body['routing_key']}",
        "status": "success",
        'message': message
    }
    
import json
import logging

logger = logging.getLogger('elastic-logger')

def log_to_elasticsearch(log_data, log_level):
    if log_level == 'info':
        logger.info(json.dumps(log_data))
    elif log_level == 'error':
        logger.error(json.dumps(log_data))
        
