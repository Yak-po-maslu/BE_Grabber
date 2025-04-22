# middlewares/logout_if_cookies_exist.py

from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
import logging
logger = logging.getLogger(__name__)
# внутри if



class LogoutIfCookiesExistMiddleware(MiddlewareMixin):
    def process_response(self, request, response: HttpResponse):
        access_token = request.COOKIES.get("access_token")
        refresh_token = request.COOKIES.get("refresh_token")

        # Если пользователь не аутентифицирован, но токены есть — удаляем их
        if not request.user.is_authenticated and (access_token or refresh_token):
            response.delete_cookie("access_token")
            response.delete_cookie("refresh_token")
            logger.debug("Cookies deleted from nonauthenticated user.")

        return response
