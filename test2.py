

from flask import Flask, request, jsonify
import requests

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
    return jsonify({'url': url_data})

if __name__ == '__main__':
    app.run(debug=True)