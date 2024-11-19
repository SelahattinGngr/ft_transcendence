from django.http import JsonResponse

from .Messages import Messages


class ResponseService:
    def create_success_response(data, status_code = 200):
        return JsonResponse(
            {"status": True, "status_code": 200, "data": data}, status=status_code
        )

    def create_error_response(error_message, language, status_code,type):
        return JsonResponse(
            {
                "status": False,
                "status_code": status_code,
                "error": Messages.get_message(error_message, language),
            },
            status=status_code,
        )

    def create_response(bool, status, message, language, status_code):
        return JsonResponse(
            {
                "status": bool,
                "status_code": status_code,
                "data": {status: Messages.get_message(message, language)},
            },
            status=status_code,
        )
