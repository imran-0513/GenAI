import os
from iso639 import Language
import requests

cog_key = "6501a1c0e4e645cfb0f152c138791bd0"
cog_region = "eastus"
translator_endpoint = "https://api.cognitive.microsofttranslator.com/"

folder_name = "reviews"

for file_name in os.listdir(folder_name):
    print("\n-----------\n"+file_name+":")
    text = open(os.path.join(folder_name,file_name),encoding="utf8").read().lower()
    print("\n"+text)

    path = "/detect"
    url = translator_endpoint+path
    params = {"api-version":"3.0"}
    headers = {
        "Ocp-Apim-Subscription-key":cog_key,
        "Ocp-Apim-Subscription-Region":cog_region,
        "Content-Type":"application/json"
    }

    body = [{"text":text}]
    request = requests.post(url,params=params,headers=headers,json=body)
    response = request.json()
    print("Language of Review is in: ",response[0]["language"])

    ##### convert the reviews in english if it its not in english ###
    language = response[0]["language"]

    if language !="en":
        path = "/translate"
        url = translator_endpoint+path
        params = {"api-version":"3.0",
                  "from":language,
                  "to":["en"]}
        
        headers = {
        "Ocp-Apim-Subscription-key":cog_key,
        "Ocp-Apim-Subscription-Region":cog_region,
        "Content-Type":"application/json"
        }

        body = [{"text":text}]
        request = requests.post(url,params=params,headers=headers,json=body)
        response = request.json()
        print("\nTranslated review: ",response[0]["translations"][0]['text'])









