import re
import string

def extract_urls(text):
    # Define a regular expression for matching URLs
    url_pattern = re.compile(
        r'http[s]?://'  # HTTP or HTTPS
        r'(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'  # Domain name
    )
    
    # Find all URLs in the text
    urls = re.findall(url_pattern, text)
    
    # Create a string of characters to remove
    chars_to_remove = string.punctuation  # This contains all punctuation characters
    chars_to_keep = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/'
    for char in chars_to_keep:
        chars_to_remove = chars_to_remove.replace(char, '')
    
    cleaned_urls = []
    for url in urls:
        # Remove trailing characters that are not alphabets, numbers, or "/"
        cleaned_url = url.rstrip(chars_to_remove)
        cleaned_urls.append(cleaned_url)
    
    return cleaned_urls