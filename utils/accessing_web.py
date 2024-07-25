import utils.api_keys as ak
import urllib.parse
import requests

API_KEYS = ak.websearch()
CX = 'e2240426e922d4188'

def get_web_results(query, api_num):
    API_KEY = API_KEYS[api_num % len(API_KEYS)]
    encoded_query = urllib.parse.quote(query)
    
    url = f'https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={CX}&q={encoded_query}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        results = response.json()
        return_list = []
        
        if 'items' in results:
            for item in results['items'][:3]:
                return_list.append({
                    'title': item.get('title', 'None'),
                    'link': item.get('link', 'None')
                })
        
        # Pad with None if less than 3 results
        while len(return_list) < 3:
            return_list.append({'title': 'None', 'link': 'None'})
        
        return return_list
    
    except requests.RequestException as e:
        print(f'Failed to retrieve results: {e}')
        return [{'title': 'None', 'link': 'None'} for _ in range(3)]


# returns title, link of the top three results!