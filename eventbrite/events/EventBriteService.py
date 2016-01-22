import requests
import json
import time
from models import Category
from dateutil.parser import parse

categories_stored = False

class EventBriteService(object):
	
	def __init__(self):
		self.base_url = 'https://www.eventbriteapi.com/v3/'
		self.token = 'D5XL6OC6476ELPPFANDY'
		self.page_size = 100

	def fetch_events(self, categories, page):
		payload = {'token': self.token, 'categories': categories, 'page':page}
		payload['expand'] = 'venue'
		request = requests.get(self.base_url + 'events/search', params = payload)
		response = request.json()
		print request.url
		output = {}
		events = []
		for event in response['events']:
			p = {'name': event['name']['html']}  
			if event['logo'] is not None:
				p['image_url'] = event['logo']['url']
			p['url'] = event['url']
			p['start'] = parse(event['start']['utc'])
			try:
				p['city'] = event['venue']['address']['city']
			except:
				print 'Venue not found'
			events.append(p)

		output['events'] = events
		output['pages'] = response['pagination']['page_count']
		
		return output

	def fetch_categories(self):
		global categories_stored
		if not categories_stored:
			data = Category.objects.all().delete()
			payload = {'token':self.token}
			request = requests.get(self.base_url + 'categories', params=payload)
			data = request.json()
			for category in data['categories']:
				c = Category()
				c.name = category['name']
				c.name_localized = category['name_localized']
				c.category_id = category['id']
				c.save()
			categories_stored = True
		
		data = Category.objects.all()
		return data