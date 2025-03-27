from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from ..models import User, Category
from ..forms.profile_edit_view import ProfileUpdateForm
from django.contrib.auth import update_session_auth_hash


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = "fanlore/profile_edit.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        """Ensure the user can only update their own profile."""
        return self.request.user

    def form_valid(self, form):
        """Handle successful form submission."""
        user = form.save(commit=False)

        if form.cleaned_data.get("new_password1"):
            update_session_auth_hash(self.request, user)

        user.save()
        messages.success(self.request, "Your profile has been updated successfully.")
        return redirect(self.success_url)

    def form_invalid(self, form):
        """Handle form errors."""
        messages.error(self.request, "Please correct the errors below.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        """
        Add categories to the context data to pass them into the template.
        """
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.choices  # Pass the categories to the template
        return context
