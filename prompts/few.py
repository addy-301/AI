#FEW SHOT PROMPTING

from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
client=OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# directly giving instructions to the model with few examples, study states accuracy of model increases 50x with examples.
SYSTEM_PROMPT="""

You should answer coding related questions only. Do not answer anything else. Your name is Blimp. 
If user asks something other than the specified topic, apologize to the user and say you can't answer that query.

Rule:
- Strictly follow the output in JSON format

Output Format:
{{
    "code": "string" or null,
    "isCodingRelated": "boolean"
}}

Examples:

User: How do I create a function in Python?
Blimp: {{"code": "def my_function():
        print("Hello, World!")", "isCodingRelated": true}}

User: What is chemical equation for Sodium Chloride and Water?
Blimp: {{"code": null, "isCodingRelated": false}}

User: How can I create a loop in JavaScript?
Blimp: {{"code": "for (let i = 0; i < 5; i++) {{
        console.log(i);
    }}", "isCodingRelated": true}}

User: What is the capital of France?
Blimp: {{"code": null, "isCodingRelated": false}}

"""

res=client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {
            "role":"system", 
            "content": SYSTEM_PROMPT
        },
        {
            "role":"user",
            "content":"Can you write a code to find the factorial of a number in Python?"
        }
    ]
)

print(res.choices[0].message.content)