from django.shortcuts import render
from django.views import View


class HomeView(View):
    def get(self, request):
        return render(request, "home.html")


class CategoriesView(View):
    def get(self, request):
        return render(request, "categories.html")
    
class SearchView(View):
    def get(self, request):
        return render(request, "search.html")