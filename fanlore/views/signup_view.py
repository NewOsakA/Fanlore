from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.contrib.auth import login, get_backends
from django.contrib import messages
from ..forms.user_signup_form import SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'login/signup.html'
    success_url = reverse_lazy('signin')

    def get(self, request, *args, **kwargs):
        """Redirect authenticated user to home"""
        if request.user.is_authenticated:
            return redirect('content_list')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        """Save new user and redirect to home"""
        user = form.save()
        backend = get_backends()[0]  # Get configured authentication backend
        user.backend = f"{backend.__module__}.{backend.__class__.__name__}"
        login(self.request, user)
        messages.success(self.request, "Signup successful! Welcome.")
        return redirect('content_list')
