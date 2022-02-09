from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView
from django.http import JsonResponse

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required

from .models import Profile
from django.views import View

from django.http import QueryDict


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}")
            return redirect('blog-home')

    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {"form": form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form:
            u_form.save()
            p_form.save()
            username = u_form.cleaned_data.get('username')
            messages.success(request, f"Profile successfully updated!")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'users/profile.html', context)


class ProfileListView(ListView):
    model = Profile
    context_object_name = 'profiles'
    queryset = Profile.objects.prefetch_related('user')

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = {'profile_followings_idx': [p.id for p in self.request.user.profile.followings.all()]}
        else:
            context = {}
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class FollowingView(LoginRequiredMixin, View):
    def put(self, request, *args, **kwargs):
        is_following = int(QueryDict(request.body)['is_following'])
        if is_following == 1:
            self.request.user.profile.followings.remove(kwargs['pk'])
        else:
            self.request.user.profile.followings.add(kwargs['pk'])

        return JsonResponse({"success": True})
