from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class CustomCorsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method == 'OPTIONS':
            response = HttpResponse()
            response['Access-Control-Allow-Origin'] = ','.join([
                'http://localhost:3000',
                'https://deep-ai.net',
                'https://www.deep-ai.net',
            ])
            response['Access-Control-Allow-Headers'] = ', '.join([
                'Content-Disposition',
                'Accept-Encoding',
                'Content-Type',
                'Accept',
                'Origin',
                'Authorization',
            ])
            response['Access-Control-Allow-Methods'] = ', '.join([
                'DELETE',
                'GET',
                'OPTIONS',
                'PATCH',
                'POST',
                'PUT',
            ])
            return response
        else:
            return None

    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = ','.join([
            'http://localhost:3000',
            'https://deep-ai.net',
            'https://www.deep-ai.net',
        ])
        response['Content-Type'] = 'application/json'
        return response
