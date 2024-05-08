# Multiagent Autogen 2.0

Multiagent Autogen 2.0 is a Streamlit-based application for managing workflows and facilitating communication among agents. It allows users to create workflows, define goals, and add agents with specific personas or instructions.

## Features

- **Workflow Management**: Create, view, and manage workflows easily.
- **Agent Management**: Add agents to workflows, specifying their names and personas/instructions.
- **Real-time Communication**: Communicate with agents through a chat interface.

## Getting Started

## Prerequisites

- Python 3.x
- pip

### Installation
1. Clone the repository:


2. Create a virtual environment:
    ```
    python -m venv venv
    ```

3. Activate the virtual environment:
- On Windows:
  ```
  venv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source venv/bin/activate
  ```

4. Install dependencies:
    ```
    pip install streamlit
    ```

### Running the Application

Once the virtual environment is activated, run the following command to start the Streamlit server:
```
streamlit run multiagent_app.py
```

## Usage

### Workflow Management

- **Creating a Workflow**: 
  - Enter the workflow name and goal.
  - Specify the number of agents for the workflow.
  - Provide details for each agent, including name and persona/instruction.
  - Click "Create Workflow" to finalize.

### Communication

- **Chat Interface**:
  - Type your message in the input box.
  - Click "Send" to communicate with agents.

## Code Structure

- `multiagent_app.py`: Main Python script containing the Streamlit application code.
- `README.md`: Documentation file providing information about the application and usage instructions.

## Dependencies

- **Streamlit**: Used for building the web application interface.

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

This project is licensed under the [MIT License](LICENSE).
