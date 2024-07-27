from celery import shared_task
import requests
import logging

from . import callbacks

logger = logging.getLogger(__name__)


@shared_task()
def sum_two_numbers(a: int, b: int) -> int:
    # This is a simple task that returns the sum of two numbers
    logger.info(f"Summing numbers: {a} + {b}")
    return a + b


@shared_task()
def query_chatgpt(prompt: str, api_key: str) -> str:
    # This task queries the ChatGPT API with a given prompt and returns the response
    logger.info(f"Querying ChatGPT with prompt: {prompt}")
    try:
        response = requests.post(
            'https://api.openai.com/v1/chat/completions', 
            json={'model': 'gpt-3.5-turbo', 'messages': [{'role': 'user', 'content': prompt}]},
            headers={'Authorization': f"Bearer {api_key}"}
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.RequestException as e:
        logger.error(f"Error querying ChatGPT: {str(e)}")
        raise


@shared_task()
def find_longest_consecutive_letters(string: str) -> int:
    # This task return the length of the longest consecutive letters in a string
    logger.info(f"Finding longest consecutive letters in string: {string}")
    max_len = 0
    current_len = 0
    previous_char = ''

    for char in string:
        if char == previous_char:
            current_len += 1
        else:
            current_len = 1
        if current_len > max_len:
            max_len = current_len
        previous_char = char

    return max_len
