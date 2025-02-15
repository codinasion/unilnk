from django.shortcuts import render
from django.views import View


class HomeView(View):
    def get(self, request):
        return render(request, "home.html")


class CategoriesView(View):
    def get(self, request):
        return render(request, "categories.html")
    
class CategoryItemsView(View):
    def get(self, request, category_str):
        return render(request, "category-items.html")
    
class SearchView(View):
    def get(self, request):
        return render(request, "search.html")
    
class ItemView(View):
    def get(self, request, item_slug):
        return render(request, "item.html")
    
class NewItemView(View):
    def get(self, request):
        return render(request, "new-item.html")