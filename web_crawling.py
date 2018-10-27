import urllib.request,re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from linkedin import linkedin
import requests
import discovery_code as dc

#[('AI technologies', 0.932564, 'https://www.dig-in.com/opinion/the-insurance-industry-is-a-prime-target-for-artificial-intelligence-technologies-and-solutions'), ('AI technologies', 0.932564, 'https://www.information-management.com/opinion/the-insurance-industry-is-a-prime-target-for-artificial-intelligence-technologies-and-solutions'), ('Fujifilm', 0.93382, 'https://www.prnewswire.com/news-releases/fujifilm-showcases-enterprise-imaging-portfolio-and-ai-initiative-at-himss-2018-300606831.html'), ('Fujifilm', 0.935818, 'http://www.prnewswire.com/news-releases/fujifilm-showcases-enterprise-imaging-portfolio-and-ai-initiative-at-himss-2018-300606831.html'), ('AI', 0.91931, 'https://www.informationweek.com/big-data/ai-machine-learning/enterprises-get-ai-head-start-with-as-a-service/d/d-id/1331369?_mc=rss%5Fx%5Fiwr%5Fedt%5Faud%5Fiw%5Fx%5Fx%2Drss%2Dsimple'), ('Machine Learning', 0.943531, 'http://www.businessofapps.com/top-five-machine-learning-trends-to-watch-out-for-in-2018/'), ('Microsoft', 0.957766, 'https://www.newkerala.com/news/fullnews-326822.html')]

            
API_KEY = '812q3vx1lwtd0d'
API_SECRET = 'hu0FcVn2y6cxVHvr'
RETURN_URL = 'https://context-switching.mybluemix.net/'
#authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL)
#authorization.state = 'your_encoded_message'
#print(authentication.authorization_url)  # open this url on your browser
#authentication.authorization_code = 'AQRbmoZH07Q9_CuhSxL5sCzkMtQUpjowPqkx24squrFaweLLtyb7598JvMRvnzKmVu-2dCYuHagjVbjanPG6COXSFz22QLyZqA7rMNmDs4rnpxh7nqW0PPNRDfqNYHgd8wGAKqfuE2V2_T4nFAjk_p7VGpiL6Q'
#authentication.get_access_token()
application = linkedin.LinkedInApplication(token='AQVRfBtQrQOhC_2x9gbhxvZSQN1UmAvX9xmngx9rhnECMqycHjwNgbg9r68e5EKDqIZrFlqdBLKYNOqyVu_QqFFG4lPizzqtXN-gQEUjAyicqwqpK8OHSi_9lNnFNSxVcCZw_LFj9AQDGryLntZoSOhb64SfGxl_lpuBZ80KHQXA6oOTjHaGdK9dE1_P_gW-2C8Hhd85Bg2TMSpXiiWWQhjTXqyOtmZJO6xRroPupKqxylUOgb59OSCGxt6FisgIpRP7gwtU4yPsBrNp6BEcxf9fSPhMRiQ_6Y0G58PXYKKujdkkXa-L37TILdof4AZThuNFl8ffNZtEaph7arI9-miI7MCDxw')

def company_detail(company):
    company_data = application.search_company(selectors=[{'companies': ['name', 'universal-name', 'website-url']}], params={'keywords': company})
    for i in company_data['companies']['values']:
        if 'websiteUrl' in i.keys():
            return(i['websiteUrl'])
            break 

subscription_key = "830999b8ba494ec48b6156eb56636484"
assert subscription_key
search_url = "https://api.cognitive.microsoft.com/bing/v7.0/search"

def get_search_results_from_bing(search_term):
    list_of_results = []
    headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
    params  = {"q": search_term, "textDecorations":True, "textFormat":"HTML","count":100}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
#    print(search_results)
#    print(len(search_results["webPages"]["value"]))
    for v in search_results["webPages"]["value"]:
        print(v["url"])
        list_of_results.append(v["url"])
        break
    return list_of_results

def intelligent_crawler(inp, parameter_list):
    name = list(inp)
#    print(name)
    if len(name) > 6:
        name = name[:6]
#    print(name)	
    name_link = [(company_detail(i),i) for i in name]
#    print(name_link)
    
    contact = []
    facebook_link =[]
    twitter_link = []
    linkedin_link = []
    name = []
    for i,j in name_link:
        name.append(j)
        contact.append(get_search_results_from_bing(j+' Contact us'))
        facebook_link.append(get_search_results_from_bing(j+' facebook'))
        twitter_link.append(get_search_results_from_bing(j+' twitter'))
        linkedin_link.append(get_search_results_from_bing(j+' linkedin'))
	
    details = []
#    print(name)
#    print(contact)
    for i,j,k,l,m,n in zip(name,name_link,contact,twitter_link,facebook_link,linkedin_link):
        d = dict({'Entity Name': '','Synopsis of Services':'','Phone':'','Contact Email':'','Other Contacts':'','Website':'','Source of Links':''})
        d['Entity Name']=i
        d['Website']=j[0]
        
        d['Contact Email']=k
        
        d['Other Contacts']= str(l)+"  "+ str(m) +"  "+ str(n)
#        print("Name",i)
#        print("Name",j)
#        print("Name",k)
        	
        synopsis_link = dc.get_synopsis_of_services(i,parameter_list)
        synopsis_link
        d['Synopsis of Services']= synopsis_link[0]
        d['Source of Links'] = synopsis_link[1]
        details.append(d)
    return details

