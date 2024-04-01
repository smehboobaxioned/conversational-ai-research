# Extract Structured Information From LLM Outputs Using OpenAI's Function Calling Feature

This folder contains an implementation of OpenAI's function calling feature. We compare the outputs of ChatGPT, with and without function calling. 
Based on a given prompt, the function calling feature not only returns the most relevant function to be used but also pre-fills the arguments needed for the function.
The use case is also implemented in Langchain ChatModel in a multiple requests setting.

## What is OpenAI's Function Calling Capability?

OpenAI's function calling feature enables developers to enhance the capabilities of language models (LLMs) such as ChatGPT. While traditional conversational features of LLMs can sometimes lead to incoherent outputs, function calling provides a more deterministic and reliable approach.

With this feature, developers can supply a list of tools and customized functions to the LLM. Instead of responding with natural language, the model returns the most relevant function based on the user prompt, along with prefilled arguments as a JSON object.

## Why Is This a Huge Update?

This feature offers several advantages and opens up new possibilities for LLM applications:

- **Controlled Responses**: Rather than generating free-form text, function calling enables the model to return specific functions, leading to more controlled and deterministic responses.
- **Structured Data Extraction**: The feature can extract structured data from text prompts and assign them as arguments to chosen functions, facilitating the processing of structured information.
- **Integration with APIs and Databases**: Developers can create their own functions that connect LLMs to internal and external APIs and databases, expanding the range of tasks that LLMs can perform.
- **User-Friendly Interaction**: Non-technical users can interact with LLMs to obtain data without needing knowledge of the underlying functions and required arguments.

## Basic Example of How to Use OpenAI Functions 

**Use case (Part 1)**: Chat models with and without function calling (gpt-3.5-turbo and gpt-4)
- We ask the model a question about a program information in a particular region and category.
- Without function calling, the chat model may respond with insufficient information or provide random responses.
- With function calling, the chat model retrieves the information from a specified function and returns an accurate answer.

## Example of How to Use These Functions to Control the Flow of a Chatbot

### Step 1: Install Required Modules
```python
# Install required Python packages using pip
!pip install openai  # Package for accessing OpenAI's GPT-3 API
!pip install langchain  # Package for working with chat models and message schemas
!pip install tiktoken
!pip install Gradio  # Package for creating interfaces for machine learning models
```
**Description:**
In this step, we ensure that the necessary Python packages are installed using `pip`. Each package serves a specific purpose within the research project.

---

### Step 2: Import Modules
```python
# Import necessary Python modules
from openai import OpenAI  # Module for accessing OpenAI's GPT-3 API
import json  # Module for working with JSON data
from datetime import datetime, timedelta  # Modules for working with dates and times
from langchain.chat_models import ChatOpenAI  # Module for defining chat models
from langchain.schema import HumanMessage, AIMessage, ChatMessage  # Modules for defining message schemas
```
**Description:**
This step involves importing Python modules required for various functionalities in the research project. Each module serves a specific purpose, such as accessing OpenAI's API, working with JSON data, handling dates and times, and defining chat models and message schemas.

---

### Step 3: Utilize OpenAI's Chat and Function Calling Features
```python
# Initialize OpenAI client with API key
client = OpenAI(api_key="XXXXXXXX") # OpenAI client instance with API key

# Send user message to GPT-3 model and retrieve response
completion = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[
        {
            "role": "user",
            "content": "What programs does TeenLife offer in Boston during the summer?",
        },
    ],
)
output = completion.choices[0].message.content
print(output)
```
**Description:**
In this step, we initialize the OpenAI client with the provided API key. We then send a user message to the GPT-3 model using the `chat.completions.create()` method and retrieve the model's response. The response is stored in the `output` variable and printed to the console.

---

### Step 4: Define and Call Functions
```python
# Define function to get program information based on region and category
def get_program_info(region, category):
    """Get program information based on the region and category"""
    program_info = {
        "region": region,
        "category": category,
        "title": "Summer TeenLife Program in Boston",
        "description": "Static description for the program by TeenLife under the Summer category",
        "sub-category": "Computer Science",
        "duration": "1 week",
        "additional-info": "xyzxyzxyzzzzzzz",
    }
    return json.dumps(program_info)

# Call the function based on parameters received from previous chat completion
category = json.loads(output.function_call.arguments).get("category")
region = json.loads(output.function_call.arguments).get("region")
params = json.loads(output.function_call.arguments)
chosen_function = eval(output.function_call.name)
program = chosen_function(**params)
print(program)
```
**Description:**
This step involves defining a function `get_program_info()` to retrieve program information based on the region and category provided. The function constructs a dictionary containing program details and returns it as a JSON string. We then call this function based on parameters received from the previous chat completion.

---

### Step 5: Prepare Responses
```python
# Prepare a human-readable response based on program information
second_completion = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=[
        {"role

": "user", "content": user_prompt},
        {"role": "function", "name": output.function_call.name, "content": program},
    ],
    functions=function_descriptions,
)
response = second_completion.choices[0].message.content
print(response)
```
**Description:**
In this step, we prepare a human-readable response based on the program information obtained from the function call. We send a message to the GPT-3 model, including the user prompt and the function call result, and retrieve the model's response. The response is stored in the `response` variable and printed to the console.



### Step 6: Use Multiple Functions for Enhanced Chatbot Interaction

```python
# Define descriptions for multiple functions
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
                    "description": "The Program title for which Student is interested for more details, e.g. Teenlife Summer Program",
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

# Define a function to interact with multiple functions
def ask_and_reply(prompt):
    """Give LLM a given prompt and get the answer."""

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[{"role": "user", "content": prompt}],
        functions=function_descriptions_multiple,
        function_call="auto",  # specify the function call in case of we want to be specific
    )

    output = completion.choices[0].message
    return output

# Scenario 1: Check program details
user_prompt = "Are there any programs in New York for Enrichment?"
output = ask_and_reply(user_prompt)

# Extract region and category from the function call
region = json.loads(output.function_call.arguments).get("region")
category = json.loads(output.function_call.arguments).get("category")

# Call the function based on the received region and category
chosen_function = eval(output.function_call.name)
program = chosen_function(region, category)

print(program)
```

**Description:**
In this step, we define descriptions for multiple functions that our chatbot can utilize. These functions include getting program information, applying for more details about a program, and submitting a review. We then define a function `ask_and_reply()` to interact with these multiple functions. Finally, we demonstrate a scenario where the chatbot checks program details for a specific region and category and then calls the appropriate function based on the received parameters.

This addition demonstrates how to handle multiple function calls within the chatbot interaction, allowing for more complex and interactive conversations.

---

These snippets, along with their descriptions, provide a detailed overview of each step in the research process. They help users understand the functionality and purpose of each code segment within the project.

##### References
1. [OpenAI Blog - Function Calling and other API updates](https://openai.com/blog/function-calling-and-other-api-updates)
2. [LangChain Documentation - Chat Models](https://python.langchain.com/docs/modules/agents/agent_types/openai_functions_agent)
3. [OpenAI CodeBook Documentation - For more code examples](https://cookbook.openai.com/examples/how_to_call_functions_with_chat_models)
