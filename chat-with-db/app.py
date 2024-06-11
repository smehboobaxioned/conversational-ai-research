import os
import time
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import streamlit as st
from sqlalchemy import create_engine

load_dotenv()

def init_database(db_type: str, user: str = None, password: str = None, host: str = None, port: str = None, database: str = None) -> SQLDatabase:
    if db_type == "mysql":
        db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    elif db_type == "supabase":
        db_uri = os.getenv("SUPABASE_DB_URI")  # SUPABASE_DB_URI should be set in your .env file
    else:
        raise ValueError("Unsupported database type. Choose 'mysql' or 'supabase'.")

    engine = create_engine(db_uri)
    return SQLDatabase(engine)

def get_sql_chain(db):
    template = """
        You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
        Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.

        <SCHEMA>{schema}</SCHEMA>

        Conversation History: {chat_history}

        Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.

        For example:
        Question: which 3 artists have the most tracks?
        SQL Query: SELECT "ArtistId", COUNT(*) as "track_count" FROM "Track" GROUP BY "ArtistId" ORDER BY "track_count" DESC LIMIT 3;
        Question: Name 10 artists
        SQL Query: SELECT "Name" FROM "Artist" LIMIT 10;

        Your turn:

        Question: {question}
        SQL Query:
    """

    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatOpenAI(model="gpt-4o")

    def get_schema(_):
        return db.get_table_info()

    return (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | llm
        | StrOutputParser()
    )

def get_response(user_query: str, db: SQLDatabase, chat_history: list):
    sql_chain = get_sql_chain(db)

    template = """
        You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
        Based on the table schema below, question, sql query, and sql response, write a natural language response.
        <SCHEMA>{schema}</SCHEMA>

        Conversation History: {chat_history}
        SQL Query: <SQL>{query}</SQL>
        User question: {question}
        SQL Response: {response}"""

    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatOpenAI(model="gpt-4o")

    chain = (
        RunnablePassthrough.assign(query=sql_chain).assign(
            schema=lambda _: db.get_table_info(),
            response=lambda vars: db.run(vars["query"]) if is_read_query(vars["query"]) else "Invalid query: Only read queries are allowed."
        )
        | prompt
        | llm
        | StrOutputParser()
    )

    response = chain.invoke({
        "question": user_query,
        "chat_history": chat_history,
    })

    if response == "Invalid query: Only read queries are allowed.":
        return response

    return response

def is_read_query(query: str) -> bool:
    read_only_keywords = ["SELECT", "SHOW", "DESCRIBE", "EXPLAIN"]
    query = query.strip().upper()
    return any(query.startswith(keyword) for keyword in read_only_keywords)

def show_sample_prompts():
    sample_prompts = [
        "📊 What are the key highlights happen in last month?",
        "💳 What payment methods were used most?",
        "🛒 How many orders were completed in last month?",
        "💳 How many units were sold in the last order?",
    ]

    st.write("Here are some questions you can ask:")
    cols = st.columns(len(sample_prompts))
    for idx, prompt in enumerate(sample_prompts):
        button_style = """
        <style>
        div.stButton > button {
            height: auto;
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 10px;
            text-align: left;
        }
        </style>
        """
        st.markdown(button_style, unsafe_allow_html=True)
        if cols[idx].button(prompt):
          with st.spinner("Generating response..."):
            if "db" in st.session_state:
              response = get_response(prompt, st.session_state.db, st.session_state.chat_history)
              st.session_state.chat_history.append(HumanMessage(content=prompt))
              st.session_state.chat_history.append(AIMessage(content=response))
              st.session_state.prompt_clicked = True
              st.experimental_rerun()

def connect_to_supabase():
    msg = st.toast('Gathering Credentials...', icon="🔑")
    time.sleep(1)
    msg.toast('Establishing Connection with Database...', icon="🔐")
    db = init_database(db_type="supabase")
    st.session_state.db = db
    msg.toast('Connection Established!!!', icon="✨")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello and welcome to DB InfoChat! I'm here to help you get insights from your database. Ask me anything, and I'll find the answers for you."),
    ]

st.set_page_config(page_title="DB InfoChat", page_icon=":speech_balloon:")
st.session_state.sample_prompt_loaded = False

# Custom CSS to hide the sidebar by default and increase container size
st.markdown(
    """
    <style>
    /* Hide the sidebar by default */
    [data-testid="stSidebar"] {
      display: none;
    }

    /* Increase the container width */
    .main .block-container {
        max-width: 1200px;
        padding-top: 1rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 1rem;
    }
    
    [data-testid="stBottomBlockContainer"] {
       max-width: 1200px;
        padding-top: 1rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("✨ DB InfoChat")

if "db" not in st.session_state:
    connect_to_supabase()

with st.sidebar:
    st.subheader("DB Settings")
    st.write("This is a simple chat application using MySQL. Connect to the database and start chatting.")

    db_type = st.selectbox("Database Type", ["mysql", "supabase"])
    if db_type == "mysql":
        host = st.text_input("Host", value="localhost", key="Host")
        port = st.text_input("Port", value="3306", key="Port")
        user = st.text_input("User", value="root", key="User")
        password = st.text_input("Password", type="password", value="rootroot", key="Password")
        database = st.text_input("Database", value="chatwithdb", key="Database")

    if st.button("Connect"):
      with st.spinner("Connecting to database..."):
        if db_type == "mysql":
          db = init_database(
              db_type,
              user=user,
              password=password,
              host=host,
              port=port,
              database=database
          )
        else:
          db = init_database(db_type)
        st.session_state.db = db
        st.success("Connected to database!")

# Display initial message and sample prompts if no prompt has been clicked
if "prompt_clicked" not in st.session_state  or not st.session_state.prompt_clicked:
  for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
      with st.chat_message("AI"):
        st.markdown(message.content)
    elif isinstance(message, HumanMessage):
      with st.chat_message("Human"):
        st.markdown(message.content)
else:
  for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
      with st.chat_message("AI"):
        st.markdown(message.content)
    elif isinstance(message, HumanMessage):
      with st.chat_message("Human"):
        st.markdown(message.content)

user_query = st.chat_input("Type your question...")
if user_query is not None and user_query.strip() != "":
  # Clear chat history - sample prompts
  st.session_state.chat_history = [
    AIMessage(content="Hello and welcome to DB InfoChat! I'm here to help you get insights from your database. Ask me anything, and I'll find the answers for you."),
  ]
  st.session_state.prompt_clicked = True
  st.session_state.chat_history.append(HumanMessage(content=user_query))
  
  with st.chat_message("Human"):
    st.markdown(user_query)

  # with st.chat_message("AI:"):
  #   with st.spinner("Generating response..."):
  #     response = get_response(user_query, st.session_state.db, st.session_state.chat_history)
  #   st.markdown(response)
  
  with st.spinner("Generating response..."), st.chat_message("AI"):
    response = get_response(user_query, st.session_state.db, st.session_state.chat_history)
    st.markdown(response)

  st.session_state.chat_history.append(AIMessage(content=response))
  
# Show sample prompts only if no user input is received
if not st.session_state.get('prompt_clicked', False):
    show_sample_prompts()
