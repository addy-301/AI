from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

def get_weather(city: str):
    url=f"https://wttr.in/{city.lower()}?format=%C+%t"
    res=requests.get(url)
    if res.status_code==200:
        return f"The weather in {city} is {res.text}"
    else:
        return "Unable to fetch weather data."


def main():
    query=input("> ")
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {
                "role": "user",
                "content": query
            }
        ]
    )
    print(f"-> {response.choices[0].message.content}")

print(get_weather("mumbai"))