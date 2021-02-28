from django.views import View
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib import messages
from .forms import SignUpForm

from .models import User


class ProfileView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'boards/_board.html')


class SignUpView(CreateView):
    model = User
    http_method_names = ['post', 'get']

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.name = request.POST.get('name', None)
            data.save()
            messages.success(request, '회원가입이 완료되었습니다.')
            return redirect('/accounts/login')
        else:
            error_data = {**form.errors.get_json_data()}
            error_message = dict()
            for i in error_data:
                for j in error_data[i]:
                    error_message[i] = j['message']

            messages.error(request, error_message)
            return render(request, 'registration/signup.html', {'data': request.POST})

    def get(self, request, *args, **kwargs):
        return render(request, 'registration/signup.html')