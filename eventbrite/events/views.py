from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import requests
# Create your views here.

def index(request):
	print request.POST
	context = {}
	return render(request, 'events/templates/index.html', context)

def show_events(request):
	print request.POST
	print request.POST.getlist('categories')
	for x in request.POST.getlist('categories'):
		print x
	categories = ','.join(x for x in request.POST.getlist('categories'))
	r = requests.get('https://www.eventbriteapi.com/v3/events/search?categories='+categories+'&token=D5XL6OC6476ELPPFANDY')	
	
	response = r.json()
	output = []
	for event in response['events']:
		p = [event['name']['html']]  
		if event['logo'] is not None:
			p.append(event['logo']['url'])
		output.append(p)
	return render_to_response('events.html', {'events':output})	