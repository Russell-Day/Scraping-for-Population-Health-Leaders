"""
At the command line, only need to run once to install the package via pip:

"""
import google.generativeai as genai
import utils.api_keys as ak
import utils.prompts as prompts
from ratelimit import limits, sleep_and_retry


# 30 calls per minute
CALLS = 42
RATE_LIMIT = 60


@sleep_and_retry
@limits(calls=8, period=60)
def get_health_leaders(query, apiNum):
  #         russellday422                               dussellray                                 akidaan                                    russellgday1                                farisday.999
  api_key = ak.gemini_keys()
  genai.configure(api_key = api_key[apiNum % 4])

    # Create the model
  # See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
  generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 16000,
    "response_mime_type": "text/plain",
  }

  model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    system_instruction=prompts.sys_prompt(),
  )

  chat_session = model.start_chat(
    history=[
    ]
  )

  try:
    if query != "None" and query is not None:
      prompt = prompts.usr_prompt(query, apiNum).strip()
      response = chat_session.send_message(prompt) #prompts.abstract_sentiment(abstract))
      if response.text.strip() == "unusual behavior notice":
        return f"Unusual behavior notice: {prompt}"
      return response.text.strip()
    else:
      # maybe return the pubmed link instead to help with mapping urself
      return "Query was not generated"
  except Exception as e:
    return f"Unable to generate because of {str(e)}"


@sleep_and_retry
@limits(calls=15, period=60)
def clean_text(text, apiNum):
  #         russellday422                               dussellray                                 akidaan                                    russellgday1                                farisday.999
  api_key = ak.gemini_keys()
  genai.configure(api_key = api_key[4 + apiNum % 2])

  # Create the model
  # See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
  generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 16000,
    "response_mime_type": "text/plain",
  }

  model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    system_instruction=prompts.sys_prompt_cleaning(),
  )

  chat_session = model.start_chat(
    history=[
    ]
  )

  try:
    if text != "None" and text is not None and text.strip() != '{"data":null,"code":402,"name":"InsufficientBalanceError","status":40203,"message":"Account balance not enough to run this query, please recharge.","readableMessage":"InsufficientBalanceError: Account balance not enough to run this query, please recharge."}':
      response = chat_session.send_message(text)
      print (f"Gemini Cleaning: {response.text.strip()[:30]}")      
      return response.text.strip()
    else:
      # maybe return the pubmed link instead to help with mapping urself
      return "None"
  except Exception as e:
    print(f"Unable to generate because of {str(e).strip()}")
    return text
