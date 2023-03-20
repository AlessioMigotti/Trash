from django.shortcuts import render
from django.views import View
# Create your views here.

class index (View):
    def get(self, request, *args, **kwargs):
        return render(request,'client/index.html')

class About(View):
    def get(self, request, *args, **kwargs):
        return render(request,'client/about.html')
