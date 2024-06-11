# Chat with Your Database

This project is a Streamlit application that allows users to interact with their SQL databases through a conversational interface. Using OpenAI's GPT-4 model and LangChain, users can ask questions about their database, and the application will generate and execute SQL queries to provide the answers.

## Features

- **Supports Multiple Databases**: Currently supports MySQL and Supabase.
- **Natural Language Processing**: Utilizes OpenAI's GPT-4 model to understand and generate SQL queries from natural language questions.
- **Interactive Interface**: Built with Streamlit to provide an easy-to-use interface.
- **Example Prompts**: Offers sample prompts to help users get started.

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/smehboobaxioned/conversational-ai-research.git
    cd chat-with-db
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**
    Create a `.env` file in the root directory and add your Supabase database URI:
    ```env
    SUPABASE_DB_URI=your_supabase_db_uri
    ```

## Usage

1. **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```

2. **Connect to a Database:**
    - Navigate to the sidebar in the Streamlit app.
    - Select the database type (MySQL or Supabase).
    - If using MySQL, enter your database credentials (host, port, user, password, database).
    - Click on "Connect" to establish the connection.

3. **Ask Questions:**
    - Type your question in natural language in the input box.
    - The application will convert your question into an SQL query, execute it, and display the results.

4. **Use Sample Prompts:**
    - Click on any of the sample prompts to see how the application works.

## Code Overview

- **`init_database`**: Initializes the connection to the database.
- **`get_sql_chain`**: Generates the SQL query chain using LangChain and GPT-4.
- **`get_response`**: Processes the user query, generates the SQL, executes it, and formats the response.
- **`is_read_query`**: Checks if the SQL query is read-only.
- **`show_sample_prompts`**: Displays sample prompts to the user.
- **`connect_to_supabase`**: Handles the connection process to the Supabase database.
- **Streamlit Components**: Manages the user interface and interactions.

## Requirements

- Python 3.8+
- Streamlit
- LangChain
- OpenAI
- SQLAlchemy
- dotenv

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## Acknowledgments

- OpenAI for providing the GPT-4 model.
- LangChain for the integration utilities.
- Streamlit for the interactive interface.
