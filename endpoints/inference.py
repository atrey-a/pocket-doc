from utils.env import HUGGINGFACE_API_KEY, HUGGINGFACE_MODEL
from utils.reqs import post_request

API_URL = f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL}"
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def consult(symptoms):
    return post_request(API_URL, {"inputs": symptoms}, headers)
