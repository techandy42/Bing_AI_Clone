import requests
import json
import os

def google_search(search_term, **kwargs):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': search_term,
        'key': os.getenv('API_KEY'),
        'cx': os.getenv('CSE_ID'),
    }
    for k, v in kwargs.items():
        params[k] = v

    response = requests.get(url, params=params)
    return json.loads(response.text)

def format_search_results(results):
    output_str = ""
    i = 1
    for result in results['items']:
        output_str += f"Result {i}:\n"
        output_str += f"Title: {result['title']}\n"
        output_str += f"Link: {result['link']}\n"
        output_str += f"Snippet: {result['snippet']}\n\n"
        i += 1
    return output_str

PROMPT = """
Important Note:
- Wrap all urls in the output in <URL>. (ex: <https://example.com>)
- Do not wrap the urls in any other format, including markdown syntax.

Instruction:

- You are a helpful, web-search assistant that provides relevant information to the user in a friendly, conversational tone.
- The following are 10 query results from Google Search API.
- The query prompt was <<QUERY PROMPT>>. Please select 3 most relevant articles from the list, then output a summary of each article. Order the 3 selected articles in order of their relevancy to the query prompt.
- Your output should contain the summary of what the user asked for, and the summary of top 3 most relevant articles.
- Summary of each article should contain its title, link, and the snippet rewritten in a user-friendly manner.
- Do not include the 'Read More' section in the summaries.
- Do not mention about other search results.
- Do not include any additional notes or comments in your output.

Query Results:

<<QUERY RESULTS>>
"""

def generate_prompt_with_results(query):
    search_results = google_search(query, num=10)
    formatted_results = format_search_results(search_results)
    full_prompt = PROMPT.replace("<<QUERY PROMPT>>", query).replace("<<QUERY RESULTS>>", formatted_results)
    return full_prompt