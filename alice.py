import pinecone 

from langchain.llms import OpenAIChat
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from langchain.callbacks.base import BaseCallbackHandler

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone

import streamlit as st

from typing import Any, Dict, List
import os
from PIL import Image
from dotenv import load_dotenv
load_dotenv() #get API keys

@st.cache_resource
def makeBot(k, streaming, namespace):
    '''Set up connection to db and create the Qretrieval object
       only needs to be run once.'''

    pinecone.init(
        api_key= os.environ.get('PINECONE_API_KEY') ,  # find at app.pinecone.io
        environment=os.environ.get('PINECONE_ENV')     # next to api key in console
    )

    db = Pinecone.from_existing_index(os.environ.get('INDEX'), OpenAIEmbeddings())
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k":k, 'namespace': namespace})

    qa = RetrievalQA.from_chain_type(
                        llm=ChatOpenAI(temperature=0, streaming= (streaming == 'Yes')), #, uses 'gpt-3.5-turbo' which is cheaper and better 
                        chain_type="stuff", 
                        retriever=retriever, 
                        return_source_documents=True)
    return qa

col1, mid, col2 = st.columns([15,1,100])
col1.image('IBRS_Round.jpg', width=100)
col2.title("Gideon's Playground")

col2.caption("Use the inputs in the sidebar to experiment with Gideon's settings")
           
with st.sidebar:
    namespace = st.radio(os.environ.get('INDEX'), ('markdown-1200', 'article'), help = "For this database select the namespace for searching")
    streaming = st.radio("Stream answers?", ("Yes", "No"),horizontal=True, index=0,
                         help="Streaming shows the output as its generated like chatGPT but the cost and #tokens does not work. Turn off to see costs")
    
    k = st.number_input("How many Articles should Gideon consult", value=5, 
                        min_value=1, max_value=50, 
                        help="This determines the number of similar article chunks to use in the prompt. Increasing this adds to the knowledge available but increases the cost/time to answer the inquiry")
    
    instructions = st.text_area('Instructions for Gideon to answer the inquiry', 
                                value='You are an experienced IBRS industry analyst speaking to an IT professional in this topic.\n\n'
                                      'Provide a clear, detailed answer based on the information provided below. Do not make up answers.\n\n'
                                      'If you do not know say "I do not know"',
                                height = 300, 
                                help='This is prepended to the inquiry and provides instructions on how to answer the inqueiry. Try chaning this to get a better result.')
    
qa=makeBot(k, streaming, namespace) 
inquiry = st.text_area(f"Hi, I'm Gideon, the IBRS Analyst Chatbot? What is your inquiry?",
                       value="")
class SimpleStreamlitCallbackHandler(BaseCallbackHandler):
    """ Copied only streaming part from StreamlitCallbackHandler """
    
    def __init__(self) -> None:
        self.tokens_area = st.empty()
        self.tokens_stream = ""
        
    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        self.tokens_stream += token
        self.tokens_area.markdown(self.tokens_stream)

if inquiry:
    with get_openai_callback() as costs:
        result = qa({"query": f'{instructions} \n\n {inquiry}'}, callbacks=[SimpleStreamlitCallbackHandler()]) 
        #streaming callback handler breaks cost reporting
        if streaming == "No": 
            st.write(result['result']) 
        st.caption(f":blue[Cost {costs.total_cost*100 : 0.2f} US cents. Tokens {costs.total_tokens :,} = {costs.prompt_tokens :,} + {costs.completion_tokens :,}]")

#    st.divider()
    for source in result["source_documents"]: 
        st.markdown(f"<details><summary> {source.metadata.get('title')} ({source.metadata.get('category_name')})</summary>\n\n[Article]({source.metadata.get('URL')}) {source.metadata.get('published_date')}  \n\n{source.page_content} </details>", unsafe_allow_html=True)