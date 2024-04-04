# https://platform.openai.com/docs/guides/function-calling
# pip install openai
# pip install langchain

# Import Modules
import os
from openai import OpenAI
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, ChatMessage


load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)


# Ask ChatGPT a Question
completion = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[
        {
            "role": "user",
            "content": "What programs TeenLife offer in Boston under summer?",
        },
    ],
)

output = completion.choices[0].message.content
print(output)


# Use OpenAI’s Function Calling Feature
function_descriptions = [
    {
        "name": "get_program_info",
        "description": "Get program information based on the region and the category queried by the user",
        "parameters": {
            "type": "object",
            "properties": {
                "region": {
                    "type": "string",
                    "description": "The program region, e.g. Boston",
                },
                "category": {
                    "type": "string",
                    "description": "The program category, e.g. Summer",
                },
            },
            "required": ["region", "category"],
        },
    }
]

user_prompt = "Which Gap Year programs are available in Boston?"

completion = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[{"role": "user", "content": user_prompt}],
    functions=function_descriptions,
    function_call="auto",
)

output = completion.choices[0].message

# check if the model wanted to call a function
tool_calls = output.tool_calls

print(tool_calls)
print(output)


# Program info Function
def get_program_info(region, category):
    """Get program information based on the region and the category"""
    program_info = {
        "region": region,
        "category": category,
        "title": "Summer TeenLife Program in Boston",
        "description": "static description for the proram by TeenLife under the Summer category",
        "sub-category": "Computer Science",
        "duration": "1 week",
        "additional-info": "xyzxyzxyzzzzzzz",
    }
    print(program_info)
    return json.dumps(program_info)


# Now lets call the Function
category = json.loads(output.function_call.arguments).get("category")
region = json.loads(output.function_call.arguments).get("region")
params = json.loads(output.function_call.arguments)

chosen_function = eval(output.function_call.name)
program = chosen_function(**params)

print(program)


# Now once we get the information from the function calling lets prepare response in human redable
second_completion = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[
        {"role": "user", "content": user_prompt},
        {"role": "function", "name": output.function_call.name, "content": program},
    ],
    functions=function_descriptions,
)
response = second_completion.choices[0].message.content
print(response)


# Multiple Functions usecase
function_descriptions_multiple = [
    {
        "name": "get_program_info",
        "description": "Get program information based on the region and the category",
        "parameters": {
            "type": "object",
            "properties": {
                "region": {
                    "type": "string",
                    "description": "The program region, e.g. Boston",
                },
                "category": {
                    "type": "string",
                    "description": "The program category, e.g. Summer",
                },
            },
            "required": ["region", "category"],
        },
    },
    {
        "name": "apply_for_rfi",
        "description": "Submit RFI for inquiring more details of a particular program",
        "parameters": {
            "type": "object",
            "properties": {
                "full_name": {
                    "type": "string",
                    "description": "The name of the Student, e.g. Dustin Silvaer",
                },
                "email": {
                    "type": "string",
                    "description": "The email of the Student, e.g. dustins@email.com",
                },
                "program_title": {
                    "type": "string",
                    "description": "The Program title for which Student is inrested for more details, e.g. Teenlife Summer Program",
                },
                "program_category": {
                    "type": "string",
                    "description": "The category of the requested program, e.g. Summer",
                },
            },
            "required": ["full_name", "email", "program_title", "program_category"],
        },
    },
    {
        "name": "submit_review",
        "description": "Submit a review as a student",
        "parameters": {
            "type": "object",
            "properties": {
                "full_name": {
                    "type": "string",
                    "description": "The name of the Student, e.g. Dustin Silvaer",
                },
                "email": {
                    "type": "string",
                    "description": "The email address of the student, e.g. dustins@email.com",
                },
                "review": {
                    "type": "string",
                    "description": "Description of review",
                },
            },
            "required": ["full_name", "email", "review"],
        },
    },
]

print(function_descriptions_multiple)


# Use the Defined Function to Ask and Reply
def ask_and_reply(prompt):
    """Give LLM a given prompt and get the answer."""

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[{"role": "user", "content": prompt}],
        # add function calling
        functions=function_descriptions_multiple,
        function_call="auto",  # specify the function call in case of we wan to be specific
    )

    output = completion.choices[0].message
    # print(output)
    return output

# Scenario 1: Check program details details
user_prompt = "is there any programs in New York for Enrichment?"
output = ask_and_reply(user_prompt)
print(output)

# Get info for the next prompt

region = json.loads(output.function_call.arguments).get("region")
category = json.loads(output.function_call.arguments).get("category")
chosen_function = eval(output.function_call.name)
program = chosen_function(region, category)

print(region)
print(category)
print(program)

program_title = json.loads(program).get("title")
program_description = json.loads(program).get("description")

print(program_title)
print(program_description)

# Scenario 2: Submit an RFI for the program
user_prompt = f"I want to apply for the program {program_title} with the category {category} my name is Mehboob shaikh and email is mehboob@axioned.com"
print(user_prompt)
output2 = ask_and_reply(user_prompt)

print(output2)

# Scenario 3: Submit a review for the program
user_prompt = f"Hi this is Mehboob Shaikh and my email is mehboobs@axioned.com. I would like to share my review for this program {program_title} under the category {category}. It was a great program arranged by the TeenLife team which I enjoyed the mose and it was a great addition to my skill I would like to recomend this to all the students who are pursuing Graduation in CS."

print(user_prompt)
output3 = ask_and_reply(user_prompt)

print(output3)



# lets make it Conversational with multiple functional calls

llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))

user_prompt = """
Hi this is Mehboob Shaikh. I am High school student looking for my Gap year Program in United States.
First, I need to know What program available in US under the Gap Year category.
Please proceed to apply for that program for me.
Also, I want to submit an review for that program. It was an great experience exploring TeenLife Platform my intrested program.
my email is mehboobs@axioned.com.
Please give me a confirmation after all of these are done.
"""

first_response = llm.predict_messages(
    [HumanMessage(content=user_prompt)], functions=function_descriptions_multiple
)

print(first_response)

second_response = llm.predict_messages(
    [
        HumanMessage(content=user_prompt),
        AIMessage(content=str(first_response.additional_kwargs)),
        AIMessage(
            role="function",
            additional_kwargs={
                "name": first_response.additional_kwargs["function_call"]["name"]
            },
            content=f"Completed function {first_response.additional_kwargs['function_call']['name']}",
        ),
    ],
    functions=function_descriptions_multiple,
)

print(second_response)

third_response = llm.predict_messages(
    [
        HumanMessage(content=user_prompt),
        AIMessage(content=str(first_response.additional_kwargs)),
        AIMessage(content=str(second_response.additional_kwargs)),
        AIMessage(
            role="function",
            additional_kwargs={
                "name": second_response.additional_kwargs["function_call"]["name"]
            },
            content=f"Completed function {second_response.additional_kwargs['function_call']['name']}",
        ),
    ],
    functions=function_descriptions_multiple,
)

print(third_response)

fourth_response = llm.predict_messages(
    [
        HumanMessage(content=user_prompt),
        AIMessage(content=str(first_response.additional_kwargs)),
        AIMessage(content=str(second_response.additional_kwargs)),
        AIMessage(content=str(third_response.additional_kwargs)),
        AIMessage(
            role="function",
            additional_kwargs={
                "name": third_response.additional_kwargs["function_call"]["name"]
            },
            content=f"Completed function {third_response.additional_kwargs['function_call']['name']}",
        ),
    ],
    functions=function_descriptions_multiple,
)

print(fourth_response)