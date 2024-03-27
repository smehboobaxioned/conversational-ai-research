# Import necessary libraries
from openai import OpenAI
import csv
import json
import numpy as np
from collections import defaultdict

# Initialize OpenAI client
client = OpenAI(api_key="your_api_key")

# Load CSV data and convert to JSONL format
csv_file_path = '/path/to/your/csv_file.csv'  # Update with your CSV file path
cleaned_data = []

with open(csv_file_path, 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        for cell in row:
            try:
                cell = cell.replace('["', '').replace('"]', '').replace('\\"', '"')
                cell_json = json.loads(cell)
                cleaned_data.append(cell_json)
            except json.JSONDecodeError as e:
                print(f"JSON decode error for cell '{cell}': {e}")

jsonl_file_path = '/path/to/your/jsonl_file.jsonl'  # Update with your JSONL file path
with open(jsonl_file_path, 'w', encoding='utf-8') as jsonl_file:
    for item in cleaned_data:
        jsonl_file.write(json.dumps(item) + '\n')

# Load dataset from JSONL file
data_path = '/path/to/your/jsonl_file.jsonl'  # Update with your JSONL file path
with open(data_path) as f:
    dataset = [json.loads(line) for line in f]

# Token counting and validation
n_missing_system = 0
n_missing_user = 0
n_messages = []
convo_lens = []
assistant_message_lens = []

def num_tokens_from_messages(messages, tokens_per_message=3, tokens_per_name=1):
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(value.split())
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3
    return num_tokens

def num_assistant_tokens_from_messages(messages):
    num_tokens = 0
    for message in messages:
        if message["role"] == "assistant":
            num_tokens += len(message["content"].split())
    return num_tokens

def print_distribution(values, name):
    print(f"\n#### Distribution of {name}:")
    print(f"min / max: {min(values)}, {max(values)}")
    print(f"mean / median: {np.mean(values)}, {np.median(values)}")
    print(f"p5 / p95: {np.percentile(values, 5)}, {np.percentile(values, 95)}")

for ex in dataset:
    messages = ex["messages"]
    if not any(message["role"] == "system" for message in messages):
        n_missing_system += 1
    if not any(message["role"] == "user" for message in messages):
        n_missing_user += 1
    n_messages.append(len(messages))
    convo_lens.append(num_tokens_from_messages(messages))
    assistant_message_lens.append(num_assistant_tokens_from_messages(messages))

print("Num examples missing system message:", n_missing_system)
print("Num examples missing user message:", n_missing_user)
print_distribution(n_messages, "num_messages_per_example")
print_distribution(convo_lens, "num_total_tokens_per_example")
print_distribution(assistant_message_lens, "num_assistant_tokens_per_example")
n_too_long = sum(l > 4096 for l in convo_lens)
print(f"\n{n_too_long} examples may be over the 4096 token limit, they will be truncated during fine-tuning")

# Upload data for training into OpenAI
training_response = client.files.create(
    file=open(jsonl_file_path, "rb"),
    purpose="fine-tune"
)

# Create Fine-Tuning Job
response = client.fine_tuning.jobs.create(
    training_file=training_response.id,
    model="gpt-3.5-turbo",
    suffix="your_suffix_name",
)

# Retrieve Fine-Tuning Job State
job_id = response.id
our_job_response = client.fine_tuning.jobs.retrieve(job_id)
print(our_job_response)
print(our_job_response.status)

# Retrieve Fine-Tuned Model ID
fine_tuned_model_id = our_job_response.fine_tuned_model
print("Fine-tuned model ID:", fine_tuned_model_id)

# Test the Fine-Tuned Model
test_messages = [
    {"role": "system", "content": "System message."},
    {"role": "user", "content": "User message."}
]

chat_response = client.chat.completions.create(
    model=fine_tuned_model_id,
    messages=test_messages,
    temperature=0.5,
    max_tokens=150
)
print(chat_response.choices[0].message.content)
