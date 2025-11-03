import streamlit as st
from groq import Groq
import os

# Try to import Google Colab userdata for secrets
try:
    from google.colab import userdata
    GROQ_API_KEY = userdata.get('GROQ_API_KEY')
except:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")

# Page configuration
st.set_page_config(
    page_title="GROQ Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stTextInput > div > div > input {
        background-color: #1e2130;
        color: #ffffff;
        border-radius: 10px;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        border: none;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20%;
    }
    .assistant-message {
        background-color: #1e2130;
        color: #ffffff;
        margin-right: 20%;
        border: 1px solid #2d3142;
    }
    .message-header {
        font-weight: bold;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "groq_api_key" not in st.session_state:
    st.session_state.groq_api_key = GROQ_API_KEY

# Sidebar
with st.sidebar:
    st.title("Configuration")
    
    # API Key input - Check for secrets from Colab or Hugging Face
    if st.session_state.groq_api_key:
        st.success("API Key loaded from secrets")
        if st.button("Use Different API Key", use_container_width=True):
            st.session_state.groq_api_key = "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"
            st.rerun()
    else:
        api_key = st.text_input(
            "GROQ API Key",
            type="password",
            help="Enter your GROQ API key"
        )
        
        if api_key:
            st.session_state.groq_api_key = api_key
            st.rerun()
    
    # Model selection
    model = st.selectbox(
        "Select Model",
        [
            "llama-3.3-70b-versatile",
            "llama-3.1-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768",
            "gemma2-9b-it"
        ],
        help="Choose the AI model for your chatbot"
    )
    
    # Temperature slider
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Higher values make output more random"
    )
    
    # Max tokens
    max_tokens = st.slider(
        "Max Tokens",
        min_value=256,
        max_value=8192,
        value=1024,
        step=256,
        help="Maximum length of the response"
    )
    
    st.divider()
    
    # Clear chat button
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    st.markdown("### About")
    st.info("This chatbot uses GROQ's ultra-fast inference API to provide lightning-quick responses. Built with Streamlit for a seamless experience.")

# Main chat interface
st.title("🤖 GROQ AI Chatbot")
st.markdown("*Powered by GROQ's Lightning-Fast Inference*")

# Check if API key is provided
if not st.session_state.groq_api_key:
    st.warning("Please enter your GROQ API key in the sidebar to start chatting.")
    st.info("Don't have an API key? Get one at [console.groq.com](https://console.groq.com)")
else:
    # Initialize GROQ client
    try:
        client = Groq(api_key=st.session_state.groq_api_key)
        
        # Display chat messages from history
        for idx, message in enumerate(st.session_state.messages):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Type your message here..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get AI response
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                
                try:
                    # Call GROQ API
                    chat_completion = client.chat.completions.create(
                        messages=st.session_state.messages,
                        model=model,
                        temperature=temperature,
                        max_tokens=max_tokens
                    )
                    
                    response = chat_completion.choices[0].message.content
                    
                    # Display assistant response
                    message_placeholder.markdown(response)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    error_message = f"Error: {str(e)}"
                    message_placeholder.error(error_message)
                    st.info("Please check your API key and try again.")
    
    except Exception as e:
        st.error(f"Failed to initialize GROQ client: {str(e)}")
        st.info("Please verify your API key is correct.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>Built with using Streamlit and GROQ</div>",
    unsafe_allow_html=True
)
