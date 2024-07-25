from groq import Groq
import utils.prompts as prompts
import utils.api_keys as ak
from ratelimit import limits, sleep_and_retry
# mixtral and gemma were taken out cause terrible
models = ["llama3-70b-8192", "llama3-8b-8192", "gemma2-9b-it"]
            # dussellray                                            russday
apikeys = ak.llama_keys()
token_limit = 1000

@sleep_and_retry
@limits(calls=6, period=60)
def get_health_leaders(query, api_num):
    client = Groq(api_key = apikeys[api_num % 3])
    try:
        if query != "None" and query is not None:
            chat_completion = client.chat.completions.create(
            #
            # Required parameters
            #
            messages=[
                # Set a user message for the assistant to respond to.
                {
                    "role": "system",
                    "content": prompts.sys_prompt(), #prompts.abstract_sentiment_groq_sys()
                },
                {
                    "role": "user",
                    "content": prompts.usr_prompt(query), #prompts.abstract_groq_usr(abstract),
                }
            ],

            # The language model which will generate the completion.
            model=models[1],

            #
            # Optional parameters
            #

            # Controls randomness: lowering results in less random completions.
            # As the temperature approaches zero, the model will become deterministic
            # and repetitive.
            temperature=0,

            # The maximum number of tokens to generate. Requests can use up to
            # 32,768 tokens shared between prompt and completion.
            max_tokens=token_limit,

            # Controls diversity via nucleus sampling: 0.5 means half of all
            # likelihood-weighted options are considered.
            top_p=1,

            # A stop sequence is a predefined or user-specified text string that
            # signals an AI to stop generating content, ensuring its responses
            # remain focused and concise. Examples include punctuation marks and
            # markers like "[end]".
            stop=None,

            # If set, partial message deltas will be sent.
            stream=False,
            )
            return chat_completion.choices[0].message.content
        else:
            return "None"
    except Exception as e:
        return "Unable to generate. " + str(e)
    
