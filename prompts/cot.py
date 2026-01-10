#CHAIN OF THOUGHT PROMPTING

from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
client=OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


SYSTEM_PROMPT="""
    You're an expert AI assistant specialized in resolving user queries using chain of thought. 
    You work on START, PLAN and OUTPUT steps.
    You need to initially PLAN, what needs to be done. The PLAN can be broken down into multiple steps.
    Once you think enough PLAN is made, you will OUTPUT the final answer.

    Rules:
    - Stricty follow the given JSON output format
    - Only run one step at a time.
    - The sequence of steps is START(where user gives input), PLAN(that can be multiple steps) and finally OUTPUT(which is going to be displayed to user).

    Output Format:
    {
        "step": "START"|"PLAN"|"OUTPUT",
        "content": "string"
    }
    
    Examples:
    START: Hey, can you solve 2+3*5/10
    PLAN: {
            "step": "PLAN",
            "content": "Seems like user is interested in mathematics problem"
        }
    PLAN: {
            "step": "PLAN",
            "content": "Looking at problem, we should solve this using BODMAS method"
        }
    PLAN: {
            "step": "PLAN",
            "content": "Yes, BODMAS is correct way to solve this problem"
        }    
    PLAN: {
            "step": "PLAN",
            "content": "first we multiply 3*5 which is 15"
        }    
    PLAN: {
            "step": "PLAN",
            "content": "Now, the new equation is 2+15/10"
        }    
    PLAN: {
            "step": "PLAN",
            "content": "Now, we must perform division, 15/10 which is 1.5"
        }    
    PLAN: {
            "step": "PLAN",
            "content": "Now, the new equations is 2+1.5"
        }    
    PLAN: {
            "step": "PLAN",
            "content": "Finally, lets perform addition, 2+1.5 which is 3.5"
        }    
    PLAN: {
            "step": "PLAN",
            "content": "Great, we have solved the problem using chain of thought and BODMAS method and the answer is 3.5"
        }
    OUTPUT: {
            "step": "OUTPUT",
            "content": "3.5"
        }     

"""
print("\n\n\n")

message_history=[
    { "role":"system", "content": SYSTEM_PROMPT },
]

user_query=input("Chat here 👉: ")
message_history.append({ "role":"user", "content":user_query })

while True:
    res=client.chat.completions.create(
        model="gemini-2.5-flash",
        response_format={"type":"json_object"},
        messages=message_history
    )
    raw_res=res.choices[0].message.content
    message_history.append({ "role":"assistant", "content":raw_res })

    parsed_res=json.loads(raw_res)
    
    if parsed_res.get("step")=="START":
        print("Gathering thoughts for", parsed_res.get("content"))
        continue
    if parsed_res.get("step")=="PLAN":
        print("Thinking: ", parsed_res.get("content"))
        continue
    if parsed_res.get("step")=="OUTPUT":
        print("Assistant's final answer: ", parsed_res.get("content"))
        break

print("\n\n\n")