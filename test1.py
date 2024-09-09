import pandas as pd
from duckduckgo_search import DDGS

# Create a DDGS object
search_query = "Crimes Delhi"

results = DDGS().text(
    keywords=search_query,
    region="In-en",
    safesearch="Off",
    timelimit="1d",
    max_results=10
)


try:
    href = results[0]['href']
    print(href)
except (IndexError, KeyError):
    print("Error accessing data in results")

results_df = pd.DataFrame(results)
results_df.to_csv("results.json", index=False)



# from newsapi import NewsApiClient
# newsapi = NewsApiClient(api_key='4f316b8b0cca48c0a71cdb75fe9729aa')

# # /v2/everything
# results = newsapi.get_everything(q='Bitcoin',
#                                       sources='bbc-news,the-verge',
#                                       domains='bbc.co.uk,techcrunch.com',
#                                       from_param='2024-08-10',
#                                       to='2024-09-01',
#                                       language='en',
#                                       sort_by='relevancy',
#                                       page=5)
# print(results.get('articles'))
# results_df=pd.DataFrame(results)
# results_df.to_csv("results.json", index=False)