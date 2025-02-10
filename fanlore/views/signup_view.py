from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView
from ..forms import SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  # Redirect authenticated users to home
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()  # Create the user
        user.backend = 'django.contrib.auth.backends.ModelBackend'  # Set the backend
        return super().form_valid(form)
