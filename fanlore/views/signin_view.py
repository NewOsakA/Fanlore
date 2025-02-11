from django.contrib.auth.views import LoginView
from django.shortcuts import redirect


class SignInView(LoginView):
    template_name = "login/signin.html"

    def get(self, request, *args, **kwargs):
        """Redirect authenticated user to home"""
        if request.user.is_authenticated:
            return redirect("home")  # Redirect if user is already logged in
        return super().get(request, *args, **kwargs)
