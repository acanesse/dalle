# App to display images from Dalle.

# don't forget to set the environement first:
# python3 -m venv venv
# source venv/bin/activate
# source .env

from flask import Flask, redirect, render_template, request, url_for
import openai, os, requests

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        prompt = request.form["prompt"]
        response = generate_image(prompt)
        return redirect(url_for("index", result=response))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_image(text='generate a picture of a dalle-mini'):

    # Set the API endpoint and the prompt
    api_endpoint = 'https://api.openai.com/v1/images/generations'

    # Set the headers and the payload
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}'
    }
    payload = {
        'model': 'image-alpha-001',
        'prompt': text,
        'num_images': 1,
        'size': '256x256',
        'response_format': 'url'
    }

    # Send the request and get the response
    response = requests.post(api_endpoint, headers=headers, json=payload)
    if response.status_code == 200:
        image_url = response.json()['data'][0]['url']
        print(f'Image URL: {image_url}')
    else:
        print(f'Error: {response.json()["error"]}')

    return image_url