import EventBriteService
from django.shortcuts import redirect
from django.shortcuts import render
from models import Category


def index(request):
    """
    View for displaying event category selection page.
    """
    request.session.flush()
    service = EventBriteService.EventBriteService()
    categories = service.fetch_categories()
    context = {'categories': categories}
    return render(request, 'events/templates/index.html', context)


def show_events(request):
    """
    View for displaying events for particular categories. Categories can be passed as POST param or can
    be accessed through session. If categories not present page is redirected to event selection page.
    """
    if len(request.POST.getlist('categories')) != 0:
        categories = ','.join(x for x in request.POST.getlist('categories'))
        request.session['categories'] = categories
        category_list = Category.objects.filter(category_id__in=request.POST.getlist('categories'))
        category_names = ', '.join(c.name + " " for c in category_list)
        request.session['category_names'] = category_names

    # If category not found in session, redirect to event category selection page.
    if 'categories' not in request.session:
        print "CATEGORIES NOT FOUND"
        return redirect('index')

    categories = request.session['categories']
    page = request.GET.get('page')

    # If page number is not provided, take user to page #1
    if page is None:
        page = 1
    page = int(page)

    # Call EventBrite service to fetch events
    service = EventBriteService.EventBriteService()
    output = service.fetch_events(categories, page)

    events = output
    # Pagination code
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

    return render(request, 'events.html', {'events': events})
