import streamlit as st
from services.chat_bot import init_gpt

def show_layout():
    st.title('チャット')
    _show_chat()


def _show_chat():
    agent_executor = init_gpt()
    prompt = st.chat_input('質問してください。')
    if prompt:
        result = agent_executor.invoke({'input': prompt})
        answer = result['output']
        conversation = dict(question=prompt, answer=answer)
        st.session_state['conversation_list'].append(conversation)
        for c in st.session_state['conversation_list']:
            with st.chat_message("user"):
                st.write(c['question'])
            with st.chat_message("AI"):
                st.write(c['answer'])
        
