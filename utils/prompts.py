import requests
from ratelimit import limits, sleep_and_retry
import utils.api_keys as ak
import utils.gemini15 as g15

curr_api = 0

def sys_prompt():
    return """
        Ensure your response adheres strictly to one of these three formats:
        - A list of names with their job titles separated by commas.
        - The exact phrase "unusual behavior notice"
        - The exact phrase "none found"

        Analyze the web page content and follow these instructions:     

        1. Look for people with "population health" in their title or job description and if you find any such individuals:
        - Return a list of all people who have "population health" in their title or job description.
        - Include their full name and their job title.

        2. If the page contains what seems to be an unusual behavior notice stopping the api from working properly:
        - Return only the phrase "unusual behavior notice".

        3. If you complete the analysis and find no individuals with "population health" in their title or job description:
        - Return only the phrase "none found".

        4. Prioritize these instructions in the following order:
        a) Check for unusual behavior notice first.
        b) Then search for population health individuals.
        c) Only return "none found" if steps a and b yield no results.
        """ 

def sys_prompt_cleaning():
    return "Given the content of a webpage, return word by word only the main content of the webpage."

@sleep_and_retry
@limits(calls=20, period=60)
def call_jina(query):
    try: 
        text = requests.get(f'https://r.jina.ai/{query}').text
        return text
    except requests.RequestException as e:
        return "None"



@sleep_and_retry
@limits(calls=30, period=60)
def cleaning_webpage(query, api_num):
    global curr_api
    curr_api = 0
    try: 
        headers = {
            'Authorization': f'Bearer {ak.jina_api()[curr_api]}',
        }
        text = requests.get(f'https://r.jina.ai/{query}', headers=headers).text

        if text.strip() == '{"data":null,"code":402,"name":"InsufficientBalanceError","status":40203,"message":"Account balance not enough to run this query, please recharge.","readableMessage":"InsufficientBalanceError: Account balance not enough to run this query, please recharge."}' and curr_api < len(ak.jina_api()) - 1:
            curr_api += 1
            headers = {
                'Authorization': f'Bearer {ak.jina_api()[curr_api]}',
            }
            text = requests.get(f'https://r.jina.ai/{query}', headers=headers).text
        elif text.strip() == '{"data":null,"code":402,"name":"InsufficientBalanceError","status":40203,"message":"Account balance not enough to run this query, please recharge.","readableMessage":"InsufficientBalanceError: Account balance not enough to run this query, please recharge."}' and curr_api >= len(ak.jina_api()) - 1:
            text = call_jina(query)

        print(f"Jina Text: {text[:30]}")
        remaining_text = g15.clean_text(text, api_num)
        print(f"Jina API num: {curr_api}")
        
        return remaining_text
    
    except requests.RequestException as e:
        return f"Error fetching webpage: {str(e)}"



def usr_prompt(query, api_num):
    cleaned_webpage = cleaning_webpage(query, api_num)
    if cleaned_webpage != "None" or cleaned_webpage is not None:
        return str(f"Webpage: \n {cleaned_webpage}.") 
    else:
        return "None"

