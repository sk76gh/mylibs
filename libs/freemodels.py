#class to manage free models
from langchain_openai import ChatOpenAI
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from .config import Config


# Set LANG and LC_ALL environment variables for proper UTF-8 encoding
os.environ['LANG'] = 'en_US.UTF-8'
os.environ['LC_ALL'] = 'en_US.UTF-8'
# Attempt to ensure Python's default I/O encoding is UTF-8
os.environ['PYTHONIOENCODING'] = 'utf-8'

class FreeModel():
  def __init__(self):
    return None

  def getModel(self,modelname:str):
    if modelname.lower() in  ['google']:
      model=self.getGoogleModel()
    elif modelname.lower() in ['openai']:
      model=self.getOpenAIModel()
    elif modelname.lower() in ['huggingface','hf']:
      model=self.getHuggingFaceModel()
    else:
      raise Exception("model not found")
    return model

  def getGoogleModel(self):
    return ChatGoogleGenerativeAI(
        #model="gemini-3.5-flash",
        #model="gemini-2.5-flash",
        model="gemini-3.1-flash-lite",
        #model="gemini-3.5-flash-lite",
        #model="gemini-2.5-flash-lite",
        #GOOGLE_API_KEY=os.environ['GOOGLE_API_KEY'],
        model_kwargs={"GOOGLE_API_KEY ":Config.GEMINI_API_KEY}
    )

  def getOpenAIModel(self):
    # Configure ChatOpenAI to use an ASCII-safe User-Agent via client_kwargs
    return ChatOpenAI(
        model="gpt-3.5-turbo",
        openai_api_key=Config.OPENAI_API_KEY

    )
  def getHuggingFaceModel(self):
    # First, create a HuggingFaceEndpoint instance
    hf_llm = HuggingFaceEndpoint(
        #repo_id="Qwen/Qwen2.5-7B-Instruct",
        repo_id="google/gemma-4-12B-it",
        temperature=0.1,
        huggingfacehub_api_token=Config.HF_API_KEY
    )
    # Then, pass the HuggingFaceEndpoint LLM instance to ChatHuggingFace
    return ChatHuggingFace(
        llm=hf_llm
    )