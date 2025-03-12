from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, AllowAny

class CookieTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        
       
        token = request.COOKIES.get('auth_token')
        print(token)
        if not token:
            return None 

        return self.authenticate_credentials(token)
