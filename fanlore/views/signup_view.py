# views/signup_view.py

from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from ..forms import SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()  # Create the user
        user.backend = 'django.contrib.auth.backends.ModelBackend'  # Set the backend
        login(self.request, user)  # Log the user in after signing up
        return super().form_valid(form)
