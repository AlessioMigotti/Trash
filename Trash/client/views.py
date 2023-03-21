from django.shortcuts import render
from django.views import View
# Create your views here.

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request,'client/index.html')

class About(View):
    def get(self, request, *args, **kwargs):
        return render(request,'client/about.html')

class Order(View):
    def get(self, request, *args, **kwargs):
        pass
        # get every item from each category

        #pass into context

        #render the template