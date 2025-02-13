from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import redirect


class SignInView(LoginView):
    template_name = "login/signin.html"

    def get(self, request, *args, **kwargs):
        """Redirect authenticated user to home"""
        if request.user.is_authenticated:
            return redirect("home")  # Redirect if user is already logged in
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        """Add success message after login"""
        response = super().form_valid(form)
        messages.success(self.request, f"Successfully signed in! Welcome back, {self.request.user.username}.")
        return response
