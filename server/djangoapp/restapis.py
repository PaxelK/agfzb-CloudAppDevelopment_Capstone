import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', "api_key"))
def get_request(url, **kwargs):
    print("GET from {} ".format(url))
    params = {
    "COUCH_URL": "https://95dec834-490b-4251-984e-9e290dc73246-bluemix.cloudantnosqldb.appdomain.cloud",
    "IAM_API_KEY": "bhIxaiAaAQxgOMIDgsH1BWxOSn6Lyj78R6UvrmcpnxZ3",
    "COUCH_USERNAME": "95dec834-490b-4251-984e-9e290dc73246-bluemix"
    }

    # If there are additional arguments; store them in a data json to pass to cloud function.
    kwarg_data = ""
    if(kwargs):
        kwarg_data = json.dumps(kwargs)

    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},params=params, data=kwarg_data)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    r = requests.post(url, params=kwargs, json=json_payload)
    status_code = r.text
    print("With status {} ".format(status_code))

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = {}
    # Call get_request with a URL parameter
    if(kwargs.get("st")):
        json_result = get_request(url, st=kwargs["st"])
    else:
        json_result = get_request(url)
    if json_result:
        #print(json_result.keys())
        dealers = json_result["dealerships"]
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],state=dealer["state"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_by_id_from_cf(url, id):

    json_result = get_request(url, id=id)
    if json_result["dealerships"][0]:
        dealer = json_result["dealerships"][0]
        return dealer
    return False

# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    json_result = get_request(url, id=kwargs.get("id"))
    #print("EARKAXEEEE: ", json.dumps(json_result["body"]["data"][0]))
    reviews = []
    if json_result:
        for review in json_result["body"]["data"]:
            analyzed_results = analyze_review_sentiments(review["review"])
            print("EARKAXEE: ", analyzed_results)
            if(analyzed_results["keywords"]):
                review["sentiment"] = analyzed_results["keywords"][0]["sentiment"]["label"]
            else:
                review["sentiment"] = "neutral"
            reviews.append(review)
            
    return reviews
# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    url_NLU = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/2a56c879-965e-47d5-8730-454f2a56ed25"
    api_key_NLU = "iWn1Ow4h5sBpgj7__C26Sd4hYO3Wr605iW64CnqtBCKT"

    authenticator = IAMAuthenticator(api_key_NLU)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )
    natural_language_understanding.set_service_url(url_NLU)
    response = natural_language_understanding.analyze(text=text, features=Features(keywords=KeywordsOptions(sentiment=True,emotion=True,limit=2))).get_result()
    return response
