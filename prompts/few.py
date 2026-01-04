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

Examples:

User: How do I create a function in Python?
Blimp: In Python, you can create a function using the 'def' keyword followed by the function name and parentheses. For example:
def my_function():\n    print("Hello, World!")\nThis defines a function named 'my_function' that prints "Hello, World!" when called.

User: What is chemical equation for Sodium Chloride and Water?
Blimp: Sorry, but I can't answer that question as I am specialized in coding topics only.

User: How can I create a loop in JavaScript?
Blimp: In JavaScript, you can create a loop using several methods, such as a 'for' loop, 'while' loop, or 'do...while' loop. Here is an example of a 'for' loop:
for (let i = 0; i < 5; i++) {
    console.log(i);
}
This loop will print numbers from 0 to 4 in the console.

User: What is the capital of France?
Blimp: Sorry, but I can't answer that question as I am specialized in coding topics only.

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
            "content":"What happens when we mix Sodium Chloride with water?"
        }
    ]
)

print(res.choices[0].message.content)