import logging

logger = logging.getLogger(__name__)


class LogRequestResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f"Request: {request.method} {request.path} {request.body}")
        response = self.get_response(request)
        logger.info(f"Response: {response.status_code} {response.content}")
        return response
