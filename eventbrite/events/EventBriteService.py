import requests
import json
from models import Category

categories_stored = False

class EventBriteService(object):
	
	def __init__(self):
		self.base_url = 'https://www.eventbriteapi.com/v3/'
		self.token = 'D5XL6OC6476ELPPFANDY'

	def fetch_events(self, categories):
		payload = {'token': self.token, 'categories': categories}
		request = requests.get(self.base_url + 'events/search', params = payload)
		return request.json()

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