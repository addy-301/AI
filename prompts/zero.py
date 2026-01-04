#zero shot prompting
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
client=OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# DIRECTLY GIVING INTRUCTIONS TO THE MODEL WITHOUT ANY EXAMPLES
SYSTEM_PROMPT="You should answer coding related questions only. Do not answer anything else. Your name is Blimp. If user asks something other than the specified topic, apologize to the user and say you can't answer that query."

res=client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {
            "role":"system",
            "content":SYSTEM_PROMPT
        },
        {
            "role":"user",
            "content":"Hey Blimp. can you write a c++ code to print hello?"
        }
    ]
)
print(res.choices[0].message.content)