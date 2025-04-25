import streamlit as st
from main import query_analyzer
from langchain_core.messages import HumanMessage, AIMessage

# Page configuration
st.set_page_config(
    page_title='AI Researcher',
    page_icon="🎃",
    layout='wide',
    initial_sidebar_state='expanded'
)

# Function to cache responses for faster future access
@st.cache_data(ttl=3600)  # Cache expires in 1 hour
def store_response(query: str, response: str):
    """
    Stores the query and response in the session cache.
    """
    cache_data = st.session_state.get("query_cache", {})
    cache_data[query] = response
    st.session_state["query_cache"] = cache_data

# Function to retrieve cached response
def get_cached_response(query: str):
    """
    Retrieves a cached response for a given query.
    """
    cache_data = st.session_state.get("query_cache", {})
    return cache_data.get(query, None)

def strmlt_app():
    # Initialize session state for chat history if not present
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Layout: Left for branding, Right for the chat
    left, space, right = st.columns([8, 1, 12])

    # Left section - App Branding
    with left:
        st.markdown("<p style='color: black;font-size: 30px;font-weight: bold;margin-bottom: 1px;'>AI Powered Research Agent</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: black;font-size: 20px;font-weight: bold;margin-bottom: 1px;'>We Help you to Create Research reports</p>", unsafe_allow_html=True)

    # Space in middle for separation
    with space:
        st.markdown("<br><br><br>", unsafe_allow_html=True)

    # Right section - Main Chat Interface
    with right:
        st.title("AI Researcher")

        chat_container = st.container()

        # Display chat history
        with chat_container:
            for msg in st.session_state.chat_history:
                if isinstance(msg, HumanMessage):
                    with st.chat_message("user"):
                        st.markdown(msg.content)
                elif isinstance(msg, AIMessage):
                    with st.chat_message("assistant"):
                        st.markdown(msg.content)

        # Input for user query
        user_query = st.chat_input("How can I assist in your research? 🎃")

        if user_query:
            try:
                with st.spinner("Fetching the details..."):
                    # Store user's message
                    st.session_state.chat_history.append(HumanMessage(user_query))

                    with chat_container:
                        with st.chat_message("user"):
                            st.markdown(user_query)

                    # Check for cached response
                    cached_response = get_cached_response(user_query)
                    if cached_response:
                        response = cached_response
                    else:
                        try:
                            response = query_analyzer(user_query)
                            store_response(user_query, response)
                        except Exception as e:
                            response = f"Error while processing your query: {e}"

                    # Store assistant's message
                    st.session_state.chat_history.append(AIMessage(response))

                    with chat_container:
                        with st.chat_message("assistant"):
                            st.markdown(response)

            except Exception as outer_exception:
                st.error(f"Something went wrong in the app: {outer_exception}")

if __name__ == "__main__":
    strmlt_app()