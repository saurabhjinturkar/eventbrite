from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import requests
import EventBriteService
# Create your views here.

def index(request):
	service = EventBriteService.EventBriteService()
	categories = service.fetch_categories()
	context = {'categories': categories}
	return render_to_response('events/templates/index.html', context)

def show_events(request):
	categories = ','.join(x for x in request.POST.getlist('categories'))
	service = EventBriteService.EventBriteService()
	response = service.fetch_events(categories)
	output = []
	for event in response['events']:
		p = [event['name']['html']]  
		if event['logo'] is not None:
			p.append(event['logo']['url'])
		p.append(event['url'])
		output.append(p)
	return render_to_response('events.html', {'events':output})	