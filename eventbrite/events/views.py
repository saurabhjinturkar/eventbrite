from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
import EventBriteService

from models import Category
# Create your views here.

def index(request):
    request.session.flush()
    service = EventBriteService.EventBriteService()
    categories = service.fetch_categories()
    context = {'categories': categories}
    return render(request, 'events/templates/index.html', context)

def show_events(request):
    if  len(request.POST.getlist('categories')) != 0:
        print 'Setting categories'
        categories = ','.join(x for x in request.POST.getlist('categories'))    
        request.session['categories'] = categories
        category_list = Category.objects.filter(category_id__in = request.POST.getlist('categories'))
        category_names = ', '.join(c.name + " " for c in category_list)
        print category_names
        request.session['category_names'] = category_names

    for key in request.session.keys():
        print key
    if 'categories' not in request.session:
        print "CATEGORIES NOT FOUND"
        return redirect('index')

    categories = request.session['categories']
    print categories
    service = EventBriteService.EventBriteService()

    page = request.GET.get('page')
    if page is None:
        page = 1
    page = int(page)
    
    output = service.fetch_events(categories, page)
    events = output
    if page == 1:
        events['has_previous'] = False
    else: 
        events['has_previous'] = True 
        events['previous_page_number'] = page - 1
         
    events['number'] = page 
    events['num_pages'] = events['pages']
    
    if page == events['pages']:
        events['has_next'] = False
    else:    
        events['has_next'] = True
        events['next_page_number'] = page + 1

    return render(request, 'events.html', {'events':events})    