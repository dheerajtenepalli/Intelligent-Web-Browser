"""
Importing_libraries
"""
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features
from watson_developer_cloud.natural_language_understanding_v1 import EntitiesOptions, KeywordsOptions,SentimentOptions
import requests
import json
import watson_developer_cloud
from watson_developer_cloud import DiscoveryV1
print(watson_developer_cloud.__version__)
import config as cg

"""Instantiating the discovery instance """
collection_id_for_custom_model = "news-en"
Environment_id_for_discovery = "system"


"""Instantiating Discovery service"""
discovery = DiscoveryV1(
      username="325557a2-ab98-48f5-a2a1-eb58993e5226",
      password="Q67zmpd6WF4H",
      version="2017-10-16"
    )

"""Instantiating Natural language service """
NaturalLanguageUnderstanding = NaturalLanguageUnderstandingV1(
username= "4da1a173-a8be-4e81-803a-b9ac37b74024",
password= "sOPjuY0yKuTe",
version="2017-02-27")

SubKey =  "b9456ce021d14e469b747781fba8aac9"
SearchUrl = "https://api.cognitive.microsoft.com/bing/v7.0/search"





					
def get_synopsis_of_services(company,search_parameters):
	string1  = ""	
	for each_string in search_parameters:
		string1 += each_string + " "	 	
	query = company+ " " + "Comapny" + " " + string1
	print(query)		
	search_response = discovery.query(Environment_id_for_discovery,collection_id_for_custom_model,natural_language_query =query,count = 50,highlight = "True")
	count_for_text = 0
	count_for_links = 0	
	text = ""
	source_links = ""
	for jsons in search_response["results"]:
		if count_for_text <= 0:
			text = jsons["highlight"]["text"][1].replace("<em>","").replace("</em>","")
		source_links += jsons["url"] + " "		
		count_for_links = count_for_links +1
		count_for_text+=1		
		if count_for_links >=5:
			break
	print("********",company)	
	print(source_links)
	print(text)
	return text,source_links 	


	





def build_dynamic_search_query(SearchParameters,NumberOfResultsToReturn = 5,count = 500):
	"""
	This Function Uses Bing API to Search the Whole Internet and get links which are relevant to user's query.Bing automatically ranks 		the links based on relevancy.
	"""
	"""
	Input: User Search Input
	Output:Ranked Links according to search
	"""
	WebSearchResults = []
	headers = {"Ocp-Apim-Subscription-Key" : SubKey}
	params  = {"q": SearchParameters + " Companies", "textDecorations":True, "textFormat":"HTML","count":count}
	output = requests.get(SearchUrl,headers=headers,params=params)
	output.raise_for_status()
	SearchOutput = output.json()
	for Links in SearchOutput["webPages"]["value"]:
		WebSearchResults.append(Links["url"])
		print(Links["url"])
	return WebSearchResults

def IntelligentCrawlUrl(URL):
	"""
	This Function uses IBM Watson's Natural Language Understanding API to crawl the links and get company or person names based on a 	 knowledge graph it already has.
	This Function also return Company/Person names based on relevance score by IBM Natural Language Cognitive API.
	"""
	ListOfEntityOutput = []
	try:
		response = NaturalLanguageUnderstanding.analyze(url =URL ,features=Features(entities=EntitiesOptions(emotion=True,sentiment=True,limit=250),sentiment=SentimentOptions(),keywords=KeywordsOptions(emotion=True,sentiment=True,limit=250)))
            
	except Exception as e: 
		response = {}
	
	if response:
		for EveryEntity in response["entities"]:
			if EveryEntity["type"] == "Company":
				if EveryEntity["relevance"] > 0.25:
					ListOfEntityOutput.append(EveryEntity["text"])
	print(ListOfEntityOutput)
	return ListOfEntityOutput
 

def rank_the_results_based_on_relevance(WebSearchResults,NumberOfResultsTOReturn = 5):
	"""
	This Function return relevant Entity names
	"""
	ListOFEveryEntityName = []
	for EveryLink in WebSearchResults:
		ListOFEveryEntityName.extend(IntelligentCrawlUrl(EveryLink))
		if len(set(ListOFEveryEntityName)) >= NumberOfResultsTOReturn:
			break
	print(set(ListOFEveryEntityName))
	return ListOFEveryEntityName
		
	





