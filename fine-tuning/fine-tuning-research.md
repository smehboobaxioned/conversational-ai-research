# Fine-Tuning with OpenAI's GPT Models: Research Documentation

## Overview
This documentation outlines the process and implementation of fine-tuning OpenAI's GPT models, particularly focusing on GPT-3.5, for specific tasks or domains. Fine-tuning allows customizing the model's behavior for specialized tasks beyond its pre-trained capabilities.

### Table of Contents
1. Setting Up Environment and Data Preparation
2. Data Formatting and Cleaning
3. Token Counting and Analysis
4. Fine-Tuning Job Creation
5. Monitoring Fine-Tuning Progress
6. Testing Fine-Tuned Model
7. User Interface Integration (Gradio)

## 1. Setting Up Environment and Data Preparation
- This step involves importing necessary libraries and setting up the environment for fine-tuning. Data files are accessed by mounting Google Drive.
- **Code Snippet**:
    ```python
    # Import necessary libraries
    from openai import OpenAI
    import csv
    import json
    import os
    import numpy as np
    from collections import defaultdict
    import tiktoken
    import gradio as gr

    # Mount Google Drive
    from google.colab import drive
    drive.mount('/content/drive')
    ```

## 2. Data Formatting and Cleaning
- CSV data is converted to JSONL format for compatibility with OpenAI's fine-tuning requirements. Data cleaning is performed to ensure proper JSON formatting and handle encoding issues.
- **Ensuring Consistency**: During the conversion process, we ensure that the data remains consistent and retains its original meaning. This consistency is vital for maintaining the integrity of the dataset and preventing any loss of information.
- **Handling Special Characters**: Some characters, such as quotation marks or special symbols, can cause issues during data processing. We carefully handle these special characters to ensure they don't interfere with the fine-tuning process, thereby enhancing the reliability of our AI model's training data.
- **Code Snippet**:
    ```python
    # Convert CSV data to JSONL format
    # Data cleaning process

    # Load CSV data from the drive
    csv_file_path = '/content/drive/MyDrive/Fine-Tune-Data/FineTuneDataSet.csv'
    cleaned_data = []

    # utf-8-sig (encoding issue)
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            for cell in row:
                try:
                    # Replace square brackets and inner double quotes that are problematic
                    cell = cell.replace('["', '').replace('"]', '').replace('\\"', '"')

                    # Load each cell as a JSON object
                    cell_json = json.loads(cell)

                    # Now that the content is clean, append to cleaned_data list
                    cleaned_data.append(cell_json)
                except json.JSONDecodeError as e:
                    print(f"JSON decode error for cell '{cell}': {e}")

    # Write cleaned data to a JSONL file
    jsonl_file_path = '/content/drive/MyDrive/Fine-Tune-Data/FineTuneDataSet-json.jsonl'
    with open(jsonl_file_path, 'w', encoding='utf-8') as jsonl_file:
        for item in cleaned_data:
            jsonl_file.write(json.dumps(item) + '\n')
    ```


## 3. Token Counting and Analysis
- Functions are defined to count tokens in messages and analyze their distribution. This step ensures messages comply with token limits for fine-tuning.
- In this step, we analyze the tokens within our data.
- **Epochs**: Refers to the number of times the entire dataset is passed forward and backward through the model during training.
- **Tokens**: Basic units of text processed by the model, such as words or punctuation marks.
- **Token Counting**: Process of quantifying the number of tokens present in each message or text segment within the dataset.
- **Distribution Analysis**: Examination of statistical measures such as mean, median, and percentiles to understand the spread of token lengths across the dataset.
- **Model Compatibility**: Ensuring that the dataset's token distribution aligns with the model's constraints, such as maximum token limits, to prevent issues during training.

##### Why is this step important?
1. **Ensuring Model Compatibility**: OpenAI's models have constraints on the maximum number of tokens they can process at once. By analyzing the token distribution, we ensure that our data fits within these constraints, preventing issues during fine-tuning.
2. **Optimizing Training**: Analyzing the token distribution helps us optimize the training process. We can identify patterns, outliers, or areas of improvement within the dataset, allowing us to fine-tune the model more effectively.

##### What does this step involve?
1. **Token Counting**: We count the number of tokens in each message or text segment within our dataset. This includes both the user-provided content and any additional metadata associated with the message.
2. **Distribution Analysis**: We analyze the distribution of tokens across the dataset. This includes examining statistical measures such as mean, median, and percentiles to understand the spread of token lengths and identify any potential issues.

##### How does this benefit the process?
- **Optimized Fine-Tuning**: By understanding the token distribution, we can adjust our fine-tuning strategy accordingly. This ensures that we make the most efficient use of the model's capacity and resources during training.
- **Quality Assurance**: Analyzing the token distribution helps us ensure the quality and consistency of our dataset. We can identify and rectify any anomalies or discrepancies, ensuring that the fine-tuning process proceeds smoothly.


- **Code Snippet**:
    ```python
    # Functions for token counting and analysis
    encoding = tiktoken.get_encoding("cl100k_base")

    def num_tokens_from_messages(messages, tokens_per_message=3, tokens_per_name=1):
        num_tokens = 0
        for message in messages:
            num_tokens += tokens_per_message
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += tokens_per_name
        num_tokens += 3
        return num_tokens

    def num_assistant_tokens_from_messages(messages):
        num_tokens = 0
        for message in messages:
            if message["role"] == "assistant":
                num_tokens += len(encoding.encode(message["content"]))
        return num_tokens

    def print_distribution(values, name):
        print(f"\n#### Distribution of {name}:")
        print(f"min / max: {min(values)}, {max(values)}")
        print(f"mean / median: {np.mean(values)}, {np.median(values)}")
        print(f"p5 / p95: {np.quantile(values, 0.1)}, {np.quantile(values, 0.9)}")
    ```


## 4. Fine-Tuning Job Creation
- Cleaned data is uploaded for fine-tuning on OpenAI's platform. A fine-tuning job is initiated with specified parameters like model and suffix.
- In this step, we create a fine-tuning job to adapt OpenAI's pre-trained model to our specific task or domain.
- Fine-tuning allows us to customize the model's behavior and improve its performance on our target dataset.
- By fine-tuning the model on our dataset, we can improve its performance and accuracy for our particular use case. This leads to more reliable and relevant AI-generated outputs.

- **Code Snippet**:
    ```python
    # Upload data for training into OpenAI
    training_file_name = '/content/drive/MyDrive/Fine-Tune-Data/FineTuneDataSetJSON-clean.jsonl'

    training_response = client.files.create(
    file=open(training_file_name, "rb"),
    purpose="fine-tune"
    )
    print(training_response)

    # Create Fine-Tuning Job
    suffix_name = "project-breif-bot"

    response = client.fine_tuning.jobs.create(
        training_file=training_response.id,
        model="gpt-3.5-turbo",
        suffix=suffix_name,
    )

    job_id = response.id
    print(response)
    ```

## 5. Monitoring Fine-Tuning Progress
- Ongoing fine-tuning jobs are listed, and their status is retrieved. Fine-tuned model ID is obtained for future reference.
- **Code Snippet**:
    ```python
    # List 10 fine-tuning jobs
    job_response = client.fine_tuning.jobs.list(limit=10)
    print(job_response)

    # Retrieve the state of a fine-tune
    job_id = "ftjob-MJYxLurBhjw7GdrJebPTRDnH"
    our_job_response = client.fine_tuning.jobs.retrieve(job_id)
    print(our_job_response)
    print(our_job_response.status)
    ```


## 6. Testing Fine-Tuned Model
- Test messages are prepared, and the chat completion API is called to interact with the fine-tuned model. Results are compared with the base model for evaluation.
- **Code Snippet**:
    ```python
    # Prepare the messages before calling the chat completion
    test_messages = []

    system_message = "Marv is an agent that helps users prepare Project Briefs. Returns the output in markdown format with headings."
    test_messages.append({"role": "system", "content": system_message})
    user_message = "Hey I have a task I need to create a project brief for a Marketing landing page can you please help me"
    test_messages.append({"role": "user", "content": user_message})

    print(test_messages)

    # OpenAI Chat Completion call goes here
    chat_response = client.chat.completions.create(
        model=fine_tuned_model_id,
        messages=test_messages,
        temperature=0,
        max_tokens=500
    )
    print(chat_response)
    ```

## 7. User Interface Integration (Gradio)
- A Gradio interface is created for user interaction with the fine-tuned model. The interface allows users to input project briefs and receive AI-generated responses.
- **Code Snippet**:
    ```python
    # Using Gradio created a UI to interact
    def generate_completion(user_prompt):
        hidden_context = ""
        messages = [
            {"role": "system", "content": hidden_context},
            {"role": "user", "content": user_prompt}
        ]
        ui_chat_response = client.chat.completions.create(
            model=fine_tuned_model_id,
            messages=messages,
            max_tokens=4096,
            temperature=0.4
        )
        return ui_chat_response.choices[0].message.content.strip()

    # Interface from Gradio
    iface = gr.Interface(
        fn=generate_completion,
        inputs=gr.Textbox(lines=5, placeholder='Try to create your Project brief'),
        outputs=gr.Textbox(lines=30, placeholder='Your AI generated Project brief'),
        title="Axioned PM AI Assistant",
        description="Enter your project brief and get AI-generated response."
    )

    iface.launch(share=True, debug=True)
    ```


## Conclusion
This documentation provides a detailed guide on fine-tuning OpenAI's GPT models for specific tasks, including data preparation, job creation, monitoring, testing, and integration into user interfaces. Fine-tuning enables tailoring AI models to address domain-specific requirements effectively.
