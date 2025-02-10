from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView
from ..forms.user_signup_form import SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'login/signup.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  # Redirect authenticated users to home
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()  # Create the user
        return super().form_valid(form)
