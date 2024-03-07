from .models import Category
from .forms import SearchForm

def menu_link(request):
    links=Category.objects.all()
    return dict(links=links)

def search_form(request):
    return {'search_form': SearchForm()}