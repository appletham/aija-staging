import streamlit as st
from assistant import OpenAIClient


# Function to initialize session state
def initialize_session_state(home_service, language):
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "selected_home_service" not in st.session_state:
        st.session_state.selected_home_service = home_service
    if "selected_language" not in st.session_state:
        st.session_state.selected_language = language


# Function to reinitialize client if needed
def initialize_client(home_service):
    try:
        st.session_state.client = OpenAIClient(home_service)
        st.session_state.client.update_assistant_instructions(home_service)
    except Exception as e:
        st.error(f"Failed to initialize OpenAI client: {e}")


# Function to handle the first prompt and response
def send_first_prompt(language):
    try:
        # Use a dictionary for language-based prompts to avoid multiple if-elif conditions
        prompts = {
            "English": "Hi. I'd like to book a service.",
            "Chinese": "您好，我想预定服务。",
            "Malay": "Hai, saya ingin menempah perkhidmatan."
        }

        # Set a default prompt if the selected language is not in the dictionary
        first_prompt = prompts.get(language, "Hi. I'd like to book a service.")

        # Send the first prompt and store the response
        first_response = st.session_state.client.get_response_without_streaming(first_prompt)
        st.session_state.messages = [{"role": "assistant", "content": first_response}]

        return first_response
    except Exception as e:
        st.error(f"Failed to send first prompt: {e}")


def main():
    st.title("ChatGPT-like clone")

    # Sidebar for home service selection
    home_service = st.sidebar.selectbox(
        "Please select one home service:",
        ("Aircon Cleaning", "Aircon Installation", "Aircon Troubleshooting", "Appliance Repair", "Curtain Making",
         "Electrician & Wiring", "Home Cleaning", "Laundry", "Locksmith", "Others", "Plumbing", "Pest Control",
         "Renovation", "Upholstery Cleaning"),
        index=0
    )

    language = st.sidebar.selectbox(
        "Please select a language to communicate:",
        ("English", "Chinese", "Malay"),
        index=0
    )

    # Initialize session state
    initialize_session_state(home_service, language)

    # Check if client needs to be reinitialized
    if ("client" not in st.session_state or
            st.session_state.selected_home_service != home_service or
            st.session_state.selected_language != language):
        initialize_client(home_service)
        st.session_state.selected_home_service = home_service
        st.session_state.selected_language = language

        # Send the first prompt to initiate the conversation with OpenAI's API
        send_first_prompt(language)

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle user input
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        response = st.session_state.client.get_response_without_streaming(prompt)

        with st.chat_message("assistant"):
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})


# Run the main function
if __name__ == "__main__":
    main()
