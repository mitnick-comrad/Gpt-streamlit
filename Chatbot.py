import streamlit as st
from streamlit_chat import message as st_message
import openai
from dotenv import load_dotenv

load_dotenv()
import os
OPENAI_API_KEY=os.environ.get('KEY')

# Set the OpenAI API key
OPENAI_API_KEY=os.environ['KEY']

openai.api_key = OPENAI_API_KEY

# Define function to generate response
context=[]
def model(question,y=0.43,io=5,uk=16):
    context= st.session_state.context
    import os
    ko=[]
    if y>1:
        y=0.43
    
    from langchain_community.vectorstores import FAISS
    from langchain_openai import OpenAIEmbeddings
    
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    def chunky(tex):
        s=''
        for a in tex:
            s+=a[0].page_content
            s+='\n'
            if len(s)>50000:
                break
        return s
    dr= [hp for hp in range(117)]
    import random
    random.shuffle(dr)
    for a in dr[:5]:

        if os.path.exists(f'./model/faiss_index_datamodel_{a}'):
            retriever= FAISS.load_local(f'./model/faiss_index_datamodel_{a}',embeddings)
            k= retriever.similarity_search_with_score(question,k=5)
            z=[h[1] for h in k]
            if min(z)<y:
                ko.extend(k)
            if len(ko)>uk:
                break
    ko.sort(key= lambda g: g[1])
    #print(len(ko),' ',ko[0][1])

    #print(ko[:10])

    #print(ko[0][1])
    prompt= f""" '''{chunky(ko[:io])}'''
    Within 150 words, Reffering only to above infromation answer the question from the auther's perspective as a casual and friendly essay type response in simple words with examples if any from the information above along with self-caring, in less than 300 words.

    ''' {question}''' """
    import os
    from openai import OpenAI
    client = OpenAI(

        api_key=OPENAI_API_KEY,
    )
    try:
        message=[{
                    "role": "system",
                    "content": "You are an Assistant that answer questions within 150 words from the author's perspective who is 'Thich Nhat Hanh' with empathy, emotional wellbeing and advice on how to self-reflect as per question, based on the given user information and conditions to the user questions with respect to the context provided."
                        }]
        message.extend(context)
        message.append({
                    "role": "user",
                    "content": prompt,

                })
        response = client.chat.completions.create(
            messages=message,
            
            model="gpt-3.5-turbo-0125",
        )
        st.session_state.context.append({'role':'user', 'content': question})
        st.session_state.context.append({'role':'assistant', 'content': response.choices[0].message.content})
        if len(st.session_state.context)>10:
            st.session_state.context= st.session_state.context[2:]
            
        #'''op=''
        #for chunk in response:
        #    op+=chunk.choices[0].delta.content or '''''
        return response.choices[0].message.content
    except Exception as e:
        print(e)
        return "Can't answer that might be technical error or the question is not answerable due to certain development guidelines."

# Initialize chat history if not present in session state
if "history" not in st.session_state:
    
    st.session_state.history = []

if "context" not in st.session_state:
    st.session_state.context=[]

# Set up the Streamlit UI
st.title("Thich Nhat Hanh Chatbot")

# Define function to generate response on text input
def generate_answer():
    user_message = st.session_state.input_text
    st.session_state.history.append({"message": user_message, "is_user": True})
    with st.spinner('Processing input ...'):
        message_bot = model(user_message,uk=50)
    st.session_state.history.append({"message": message_bot, "is_user": False})

# Create text input box for user interaction
st.text_input("Talk to the bot", key="input_text", on_change=generate_answer)

# Display chat history
for i, chat in enumerate(st.session_state.history):
    st_message(**chat, key=str(i))  # Unpacking
