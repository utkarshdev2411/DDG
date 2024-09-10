from flask import Flask, request, jsonify
import requests
from langchain_community.document_loaders import UnstructuredURLLoader

import os
import google.generativeai as genai 
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_news():
    # Define the base URL and parameters
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': 'crimes in Delhi',
        'from': '2024-09-06',
        'to': '2024-09-10',
        'pageSize': 1,
        'apiKey': '4f316b8b0cca48c0a71cdb75fe9729aa'
    }

    # Modify parameters based on query parameters from the request
    for key in params.keys():
        if key in request.args:
            params[key] = request.args.get(key)

    # Make the GET request to the external API
    response = requests.get(url, params=params)

    # Parse the JSON response
    data = response.json()
    
    # Extract the URL from the first article
    url_data = data['articles'][0]['url']
    
    # Return the URL as a JSON response
    news_url = [url_data]

    # Load the news data synchronously
    loader = UnstructuredURLLoader(urls=news_url)
    news_data = loader.load()[0]

    # Extract the page content from the Document object
    news_text = news_data.page_content

    prompt = (
        'You are an AI simulating a human who crafts engaging and interactive case studies based on real news events. '
        'These case studies should delve into the Indian Constitution, specifically highlighting instances where fundamental rights and laws have been violated. '
        'Your task is to integrate relevant data and legal aspects from the Constitution and provide detailed analysis without summarizing the case study. '
        'Ensure the case study is immersive, guiding the reader through an interactive exploration of the situation, encouraging critical thinking, '
        'and prompting discussion on the constitutional violations involved.'
    )

    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([prompt, news_text])

    # Convert the response to a JSON-serializable format
    response_content = response.to_dict()

    # Return the response as JSON
    return jsonify({'response': response_content})

if __name__ == '__main__':
    app.run(debug=True)