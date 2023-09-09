import openai
import tiktoken
import os
from webscraper import fetch_webpage_content

openai.api_key = os.getenv('OPENAI_API_KEY')

def get_chat_completion(prompt):
    chat_completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return chat_completion.choices[0].message.content

def count_tokens(string):
  encoding = tiktoken.get_encoding('cl100k_base')
  num_tokens = len(encoding.encode(string))
  return num_tokens

PROMPT_TEMPLATE = f"""
    Reference Material:

    -------------------
    <<FORMATTED CONTENT>>

    Instruction:

    - The above are reference material for you to provide a detailed and accurate response.
    - The below is the user prompt for you to answer accordingly.

    User Prompt:

    <<USER PROMPT>>
    """

def create_prompt_with_reference_material(url_list):
    titles = []
    contents = []
    for url in url_list:
        content, title = fetch_webpage_content(url)
        if title and content:
            titles.append(title)
            contents.append(content)
    
    # Check combined token count
    combined_str = " ".join(contents)
    num_tokens = count_tokens(combined_str)

    # Pop 200 words at a time from the last content in the list until the combined token count is at or below 4000
    while num_tokens > 4000 and contents:
        last_content_words = contents[-1].split()
        if len(last_content_words) > 200:
            contents[-1] = " ".join(last_content_words[:-200])
        else:
            contents.pop(-1)
            titles.pop(-1)
        
        # Update combined_str and num_tokens
        combined_str = " ".join(contents)
        num_tokens = count_tokens(combined_str)
    
    # Format the final contents and titles
    formatted_content = ""
    for i, (title, content) in enumerate(zip(titles, contents)):
        if content:  # Skip the title if all of its content has been popped off
            formatted_content += f"Source {i+1}: {title}\n{content}\n-------------------\n"

    # Format the prompt template
    prompt_template = PROMPT_TEMPLATE.replace("<<FORMATTED CONTENT>>", formatted_content)

    return prompt_template

def fetch_and_answer(url_list, user_input):
    # Get the prompt template with reference material
    prompt_with_ref_material = create_prompt_with_reference_material(url_list)

    # Embed the user input into the prompt template
    final_prompt = prompt_with_ref_material.replace("<<USER PROMPT>>", user_input)

    # Get the completion based on the prompt
    result = get_chat_completion(final_prompt)

    return result