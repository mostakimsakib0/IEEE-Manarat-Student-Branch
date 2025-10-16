from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import UserRegistrationForm, UserUpdateForm, SessionForm
from django.views.generic import FormView, CreateView, ListView
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import UserProfile, Session
from .forms import CustomAuthenticationForm


class UserRegistrationView(FormView):
    template_name = "accounts/registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class LoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = CustomAuthenticationForm 
    title = "Login"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("profile")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("profile")


def LogoutView(request):
    if not request.user.is_authenticated:
        return redirect("login")
    logout(request)
    return redirect("login")


class UserProfileView(View):
    template_name = "accounts/profile.html"
    title = "Profile"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("login")
        if request.user.is_superuser:
            messages.error(
                request,
                "Admin users need to update their profile from the admin panel.",
            )
            return render(request, self.template_name, {"user": request.user})
        user_profile = get_object_or_404(
            request.user.profile.__class__, user=request.user
        )
        return render(
            request, self.template_name, {"user": request.user, "profile": user_profile}
        ) 


class UserUpdateView(View):
    template_name = "accounts/update_profile.html"
    title = "Update Profile"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("login")
        if request.user.is_superuser:
            messages.error(
                request,
                "Admin users need to update their profile from the admin panel.",
            )
            return redirect("profile")
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect("login")
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
        return render(request, self.template_name, {"form": form})


class SessionView(LoginRequiredMixin, CreateView):
    model = Session
    form_class = SessionForm
    template_name = "accounts/session_form.html"
    success_url = reverse_lazy("home")


def session_list(request):
    sessions = Session.objects.all()  # or 'id' if no date
    return {"sessions": sessions}


def CommitteeListView(request, ses_slug=None):
    committees = UserProfile.objects.all().order_by("designation")
    if ses_slug is not None:
        session = Session.objects.get(slug=ses_slug)
        if session:
            committees = UserProfile.objects.filter(session=session).order_by(
                "designation"
            )
    session = Session.objects.get(slug=ses_slug)
    return render(
        request,
        "accounts/committee_list.html",
        {"committees": committees, "session": session},
    )
