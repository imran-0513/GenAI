import openai
from secret import openai_key
openai.api_key = openai_key

from dotenv import load_dotenv
load_dotenv()

def poem_on_india():
    prompt = 'write a poem on india in 4 lines'

    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = [
            {'role':'user','content':'write a poem on india in 4 lines'}
        ]
        
        )
    print(response)

    poem_on_india()
