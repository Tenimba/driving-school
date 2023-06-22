from django.contrib.auth.models import User
from gestion_cours.models import User_profil

class UserProfilMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("middleware")
        if request.user.is_authenticated:
            try:
                request.user_profil = User_profil.objects.get(user=request.user)
            except User_profil.DoesNotExist:
                request.user_profil = None
        else:
            request.user_profil = None

        response = self.get_response(request)

        return response

