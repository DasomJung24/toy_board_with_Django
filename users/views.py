from django.views import View
from django.shortcuts import render


class ProfileView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'boards/_board.html')