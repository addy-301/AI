from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import requests
from pydantic import BaseModel, Field
from typing import Optional
load_dotenv()
client=OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def run_command(cmd: str):
    res=os.system(cmd)
    return res

def get_weather(city: str):
    url=f"https://wttr.in/{city.lower()}?format=%C+%t"
    res=requests.get(url)
    if res.status_code==200:
        return f"The weather in {city} is {res.text}"
    else:
        return "Unable to fetch weather data."


available_tools={
    "get_weather": get_weather,
    "run_command": run_command
}

SYSTEM_PROMPT="""
    You're an expert AI assistant specialized in resolving user queries using chain of thought. 
    You work on START, PLAN and OUTPUT steps.
    You need to initially PLAN, what needs to be done. The PLAN can be broken down into multiple steps.
    Once you think enough PLAN is made, you will OUTPUT the final answer.
    You can also call a tool if required from the list of available tools.
    For every tool call, wait for the observe step to get the output from tool and then continue with your PLAN or OUTPUT depending on the situation.

    Rules:
    - Stricty follow the given JSON output format
    - Only run one step at a time.
    - The sequence of steps is START(where user gives input), PLAN(that can be multiple steps) and finally OUTPUT(which is going to be displayed to user).

    Output Format:
    {
        "step": "START"|"PLAN"|"OUTPUT"|"TOOL",
        "content": "string",
        "tool": "string",
        "input": "string"
    }

    Available Tools:
    - get_weather(city: str): This tool takes city name as input and returns the current weather information for that city.
    - run_command(cmd: str): This tool takes a command as input, executes it in the terminal and returns the output.
    
    Example 1:
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
    Example 2:
    START: Hey, can you tell me the weather in London?
    PLAN: {
            "step": "PLAN",
            "content": "User is asking for weather information for London"
        }
    PLAN: {
            "step": "PLAN",
            "content": "Let's see is we have a tool to get weather information."
        }
    PLAN: {
            "step": "PLAN",
            "content": "Yes, we have get_weather(city: str) tool which can be used to get weather information for London"
        }    
    PLAN: {
            "step": "PLAN",
            "content": "I need to call tool get_weather with city as London to get the weather information for London"
        }    
    PLAN: {
            "step": "TOOL",
            "tool": "get_weather",
            "input": "London"
        }    
    PLAN: {
            "step": "OBSERVE",
            "tool": "get_weather",
            "output": "The weather in London is Cloudy, 15°C"
        }    
    PLAN: {
            "step": "PLAN",
            "content": "Great, I have received the output from tool get_weather and the weather in London is Cloudy, 15°C"
        }    
    OUTPUT: {
            "step": "OUTPUT",
            "content": "The weather in London is Cloudy, 15°C"
        }     

"""
print("\n\n\n")

class OutputFormat(BaseModel):
    step: str=Field(..., description="The step can be START, PLAN, OUTPUT or TOOL")
    content: Optional[str] = Field(None, description="The content field is used to provide additional information or thoughts related to the current step.")
    tool: Optional[str] = Field(None, description="The tool field is used to specify the tool being called.")
    input: Optional[str] = Field(None, description="The input field is used to provide the input for the tool being called.")

message_history=[
    { "role":"system", "content": SYSTEM_PROMPT },
]
while True:
    user_query=input("Chat here 👉: ")
    message_history.append({ "role":"user", "content":user_query })

    while True:
        res=client.chat.completions.parse(
            model="gemini-2.5-flash",
            response_format=OutputFormat,
            messages=message_history
        )
        raw_res=res.choices[0].message.content
        message_history.append({ "role":"assistant", "content":raw_res })

        parsed_res = res.choices[0].message.parsed
        if not isinstance(parsed_res, dict):
            print("[Warning] Model response is not a JSON object:", parsed_res)
            continue
        if parsed_res.step == "START":
            print("Gathering thoughts for", parsed_res.content)
            continue

        if parsed_res.step=="TOOL":
            tool_called=parsed_res.tool
            tool_input=parsed_res.input
            print(f"> {tool_called} is called with input: {tool_input}")
            tool_result=available_tools[tool_called](tool_input)
            print(f"> {tool_called} is called with input: {tool_input}=> {tool_result}")
            message_history.append({ "role":"developer", "content": json.dumps({
                "step": "OBSERVE",
                "tool": tool_called,
                "input": tool_input,
                "output": tool_result
            }) })
            continue

        if parsed_res.step=="OBSERVE":
            print("Received output from tool:", parsed_res.output)
            continue

        if parsed_res.step=="PLAN":
            print("Thinking: ", parsed_res.content)
            continue
        
        if parsed_res.step=="OUTPUT":
            print("Assistant's final answer: ", parsed_res.content)
            break

    print("\n\n\n")