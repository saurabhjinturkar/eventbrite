import requests
from dateutil.parser import parse
from models import Category

# Variable to check if category information is stored in database
categories_stored = False


class EventBriteService(object):
    """
    Class for calling EventBrite APIs
    """

    def __init__(self):
        self.base_url = 'https://www.eventbriteapi.com/v3/'
        self.token = 'D5XL6OC6476ELPPFANDY'

    def fetch_events(self, categories, page):
        """
        Function to fetch events for given category on a given page
        Args:
            categories: category IDs to fetch. Should be comma separated string,
            page: page number to fetch

        Returns:
        map containing events
        """
        payload = {'token': self.token, 'categories': categories, 'page': page}
        payload['expand'] = 'venue'
        request = requests.get(self.base_url + 'events/search', params=payload)
        response = request.json()
        output = {}
        events = []
        for event in response['events']:
            p = {'name': event['name']['html']}
            if event['logo'] is not None:
                p['image_url'] = event['logo']['url']
                print p['image_url']
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
        """
        Fetch categories present on EventBrite.

        If categories are not cached into database, they are accessed from API and stored into database.
        Returns:

        """
        global categories_stored
        if not categories_stored:
            data = Category.objects.all().delete()
            payload = {'token': self.token}
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
