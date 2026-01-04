from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

res = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {
            "role": "system", 
            "content": "You are an expert in Chemistry and can only answer Chemistry related queries. If query is unrelated or other than the specified topic just prompt to user, 'Sorry, but I can't answer that question as I am specialized in Chemistry topics only.'"
        },
        {
            "role": "user",
            "content": "Hi, can you write a balanced chemical equation for the reaction between hydrochloric acid and sodium hydroxide?"
        }
    ]
)

print(res.choices[0].message.content)