""" Importing dependencies"""
from flask import Flask, render_template, request
import os
import discovery_code as cognitive_search
import web_crawling as wc
app = Flask(__name__,template_folder='templates')
app.secret_key = 'qwertyuiop'
ports = int(os.getenv('PORT', 8000)) #Setting port automatically
@app.route("/")
def home():
	"""Upon 
user refresh it renders html and sets all variables"""
	return render_template("index.html")

@app.route("/get")
def get_search_response():
        
	"""This is the function called by the front end when a user types a message and that message is analyzed to get bot response """
	print("calling")	
	search_parameters = request.args.get("msg")
	print(search_parameters)

@app.route('/handle_data',methods=['POST'])
def handle_data():
	search_parameters = request.form['Search_Bar_text']
	print(search_parameters)
	search_string_parameters = search_parameters.split(",")
	print(search_string_parameters)
	search_results = cognitive_search.build_dynamic_search_query(search_parameters)
	results = cognitive_search.rank_the_results_based_on_relevance(search_results)	
	#print(results)
	list_of_dict = wc.intelligent_crawler(results,search_string_parameters)
	print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
	print(list_of_dict)
	return render_template("result.html",result = list_of_dict)
	
if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=ports, debug=True)
    app.run()
