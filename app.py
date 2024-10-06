from flask import Flask, render_template
import google.generativeai as genai
from datetime import datetime
from ollama import Client
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential

app = Flask(__name__)

NICE_MESSAGE_PROMPT="Dame un frase motivadora y positiva para alguien que vive en la ciudad de Mendoza Argentina. La frase tiene que estar relacionada a un lugar o comida típica de esa ciudad. Solamente dame la frase y nada más. No expliques cómo elegiste la frase ni el significado de ella."

# these keys are hardcoded here just as a demo, in production use a secure location!
GEMINI_API_KEY = "*****"
FLY_IO_OLLAMA_URL='http://***********.dev'
AZURE_AI_STUDIO_API_KEY = "********"
AZURE_AI_STUDIO_ENDPOINT = 'https://**************.ai.azure.com'

def do_work_every_five_minutes():
    minute_as_string = f"{datetime.now().minute}"
    last_digit = int(minute_as_string[-1])
    # print (f"current minute unit {last_digit}")
    if last_digit >=1 and last_digit <= 5:
        return True
    return False

@app.route('/')
def generate_nice_message():
    # ask gemini to generate a nice message
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    nice_message ="problem generating!"
    generated_by =""

    try:
        response = model.generate_content(NICE_MESSAGE_PROMPT)
        nice_message=response.text
        generated_by ="Generated by Gemini AI"
    except Exception as e:
        # Gemini is not responding! maybe we are breaking the free tier limit (15 calls per minute)

        # quick&dirty "load balancing": call ollama-Fly.io every five minutes, or, call Azure instead
        if do_work_every_five_minutes():
            # let ollama do the work
            client = Client(host=FLY_IO_OLLAMA_URL)
            response = client.generate(model='phi3:mini', prompt=NICE_MESSAGE_PROMPT)
            nice_message=response['response']
            generated_by ="Generated by Ollama:Microsoft Phi3 running on Fly.io"
        else:
            # let Azure AI handle the work
            client = ChatCompletionsClient(
                endpoint=AZURE_AI_STUDIO_ENDPOINT,
                credential=AzureKeyCredential(AZURE_AI_STUDIO_API_KEY)
            )
            payload = {
            "messages": [
                {
                "role": "user",
                "content": NICE_MESSAGE_PROMPT
                }
            ],
            "max_tokens": 4096,
            "temperature": 0,
            "top_p": 1
            }
            response = client.complete(payload)

            nice_message=response.choices[0].message.content
            generated_by ="Generated by Microsoft Phi3 provided by Azure Serverless AI"

    return render_template('positive_message.html', nice_message=f"{nice_message} ({generated_by})")

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. You
    # can configure startup instructions by adding `entrypoint` to app.yaml.    
    app.run(host='0.0.0.0',port=7000,debug=True)