import streamlit as st

# Initialize a list to store created workflows
workflows = []

# Sidebar layout
st.sidebar.title("Workflow Management")
st.sidebar.info("No workflow available. Please create a new workflow.")

# Initialize inputs for adding agents using session_state
if 'new_agents' not in st.session_state:
    st.session_state.new_agents = [{"name": "", "persona": ""}]

# Create New Workflow form
if not workflows:
    new_workflow_name = st.sidebar.text_input("Enter Workflow Name:")
    new_workflow_goal = st.sidebar.text_area("Enter Workflow Goal:")

    # Number of agents input
    number_of_agents = st.sidebar.number_input("Number of Agents", min_value=1, max_value=5, value=1)

    class Agents:
        pass

    p = Agents()
    keys = [str("agent "+str(x+1)) for x in range(number_of_agents)]
    for key in keys:
        setattr(p, key+"_name", st.sidebar.text_input(label=f"{key.capitalize()} Name"))
        setattr(p, key+"_persona", st.sidebar.text_area(label=f"{key.capitalize()} Persona/Instruction"))

    # Create Workflow button
    create_workflow_button = st.sidebar.button("Create Workflow")

    # Create new workflow and add agents
    if create_workflow_button:
        if new_workflow_name.strip() != "" and new_workflow_goal.strip() != "":
            agents = [{"name": getattr(p, key+"_name"), "persona": getattr(p, key+"_persona")} for key in keys if getattr(p, key+"_name").strip() != ""]
            workflow = {
                "name": new_workflow_name,
                "goal": new_workflow_goal,
                "agents": agents
            }
            workflows.append(workflow)
            st.sidebar.success(f"Workflow '{new_workflow_name}' created successfully with {len(agents)} agent(s)!")
        else:
            st.sidebar.error("Please fill in all workflow fields.")
else:
    add_workflow_button = st.sidebar.button("Create New Workflow")

    # Add Workflow logic
    if add_workflow_button:
        new_workflow_name = st.sidebar.text_input("Enter Workflow Name:")
        new_workflow_goal = st.sidebar.text_area("Enter Workflow Goal:")

        # Number of agents input
        number_of_agents = st.sidebar.number_input("Number of Agents", min_value=1, max_value=5, value=1)

        class Agents:
            pass

        p = Agents()
        keys = [str("agent"+str(x+1)) for x in range(number_of_agents)]
        for key in keys:
            setattr(p, key+"_name", st.sidebar.text_input(label=f"{key.capitalize()} Name"))
            setattr(p, key+"_persona", st.sidebar.text_area(label=f"{key.capitalize()} Persona/Instruction"))

        # Create Workflow button
        create_workflow_button = st.sidebar.button("Create Workflow")

        # Create new workflow and add agents
        if create_workflow_button:
            if new_workflow_name.strip() != "" and new_workflow_goal.strip() != "":
                agents = [{"name": getattr(p, key+"_name"), "persona": getattr(p, key+"_persona")} for key in keys if getattr(p, key+"_name").strip() != ""]
                workflow = {
                    "name": new_workflow_name,
                    "goal": new_workflow_goal,
                    "agents": agents
                }
                workflows.append(workflow)
                st.sidebar.success(f"Workflow '{new_workflow_name}' created successfully with {len(agents)} agent(s)!")
            else:
                st.sidebar.error("Please fill in all workflow fields.")

# Display existing workflows
if workflows:
    st.sidebar.subheader("Existing Workflows:")
    for workflow in workflows:
        st.sidebar.write(f"- {workflow['name']}")
        st.sidebar.write(f"   Goal: {workflow['goal']}")
        st.sidebar.write("   Agents:")
        for i, agent in enumerate(workflow['agents']):
            st.sidebar.write(f"      - Agent { i+1}: Name: {agent['name']}, Persona/Instruction: {agent['persona']}")





"""
Playground area
"""

# Initialize a list to store chat messages
# Display chat interface on the right side
chat_messages = []
st.title("Multiagent Autogen 2.0 Playground")

message_input = st.text_area("Type your message here:", key="message_input")
send_button = st.button("Send")

if send_button and message_input.strip() != "":
    chat_messages.append(message_input)
    st.session_state.message_input = ""  # Clear the message input field

# Display chat messages
for message in chat_messages:
    st.write(message)