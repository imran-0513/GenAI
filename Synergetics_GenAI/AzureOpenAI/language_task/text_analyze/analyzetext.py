from azure.core.credentials import AzureKeyCredential ## used to authenticate using api key
from azure.ai.textanalytics import TextAnalyticsClient
from httplib2 import Credentials ## client class for interacting with the textanalytics service

import os 

## for text we key and endpoint

cog_key = "1944104fbe754d69bfccd7faccc590d3"

cog_endpoint = "https://text-analyze-review.cognitiveservices.azure.com/"


Credential = AzureKeyCredential(cog_key)
cog_client = TextAnalyticsClient(cog_endpoint,credential=Credential)

reviews_folder = "reviews"

for file_name in os.listdir(reviews_folder):
    print("\n.................\n"+file_name+":")

    #### read texts 
    text = open(os.path.join(reviews_folder,file_name),encoding='utf8').read()
    print("\n"+text)

    ### will check the language in which they written in
    detected_language = cog_client.detect_language(documents=[text])[0]
    print("\n Language:{}".format(detected_language.primary_language.name))

    ########## to check sentiment analysis ###################

    sentiment_analysis = cog_client.analyze_sentiment(documents=[text])[0]
    print("\n Senetiment:{}".format(sentiment_analysis.sentiment))

    ######### to get important entities ###########
    entities = cog_client.recognize_entities(documents=[text])[0].entities
    for entity in entities:
        print("\t {} ({})".format(entity.text,entity.category))
