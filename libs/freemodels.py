#class to manage free models
from langchain_openai import ChatOpenAI
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama, OllamaLLM
import os
import ollama
import subprocess
import time
import shutil
import urllib.request
import requests
from .config import Config


# Set LANG and LC_ALL environment variables for proper UTF-8 encoding
os.environ['LANG'] = 'en_US.UTF-8'
os.environ['LC_ALL'] = 'en_US.UTF-8'
# Attempt to ensure Python's default I/O encoding is UTF-8
os.environ['PYTHONIOENCODING'] = 'utf-8'

class FreeModel():
  def __init__(self):
    self.OLLAMA_URL = "http://localhost:11434"

    return None

  def getModel(self,modelname:str):
    if modelname.lower() in  ['google']:
      model=self.getGoogleModel()
    elif modelname.lower() in ['openai']:
      model=self.getOpenAIModel()
    elif modelname.lower() in ['huggingface','hf']:
      model=self.getHuggingFaceModel()
    elif modelname.lower() in ['ollama-chat']:
      model=self.getChatOllama()
    elif modelname.lower() in ['ollama']:
      model=self.getOllamaModel()
    else:
      raise Exception("model not found")
    return model

  def getChatOllama(self):
    # Configure ChatOllama to use an ASCII-safe User-Agent via client_kwargs
    MODEL_NAME="llama2-7b-chat"

    # 1. Pull the model programmatically if it doesn't exist
    print(f"Checking/Downloading {MODEL_NAME}...")
    self.ensure_ollama_server()
    ollama.pull(MODEL_NAME)

    # 2. Instantiate and use via LangChain
    llm = ChatOllama(model=MODEL_NAME)
    return llm

  def getOllamaModel(self):
    # Configure OllamaLLM to use an ASCII-safe User-Agent via client_kwargs
    MODEL_NAME="llama3.2"
    
    # 1. Pull the model programmatically if it doesn't exist
    print(f"Checking/Downloading {MODEL_NAME}...")
    self.ensure_ollama_server()
    ollama.pull(MODEL_NAME)

    # 2. Instantiate and use via LangChain
    llm = OllamaLLM(model=MODEL_NAME)
    return llm

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
  
  #methods to install ollama server, spins server
  def install_ollama_linux(self):
    """Downloads and safely executes the official Ollama Linux installer."""
    print("📥 Ollama is not installed. Attempting programmatic installation...")
    installer_url = "https://ollama.com/install.sh"
    
    try:
        # Download the installer content directly via Python
        with urllib.request.urlopen(installer_url) as response:
            installer_script = response.read().decode('utf-8')
        
        print("⚙️ Running Ollama installer script via bash...")
        # Pipe the script string directly into `sudo bash` 
        # This mirrors the official `curl -fsSL ... | sh` command perfectly
        process = subprocess.run(
            ["sudo", "bash"],
            input=installer_script,
            text=True,
            capture_output=True, # Captures stderr logs to help troubleshoot if it fails
            check=True
        )
        print("✨ Ollama binary installed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Installation failed with code {e.returncode}")
        print(f"Error details:\n{e.stderr}")
        raise RuntimeError("Failed to install Ollama automatically via streamed bash pipeline.")
    except Exception as e:
        raise RuntimeError(f"Network or permission error during download: {e}")

  def ensure_ollama_server(self):
      """Checks for installation, starts the server if down, and verifies status."""
      # 1. Check if Ollama binary exists on the system path
      if not shutil.which("ollama"):
          if os.name != 'nt' and os.uname().sysname == 'Linux':
              self.install_ollama_linux()
          else:
              raise NotImplementedError("Automatic installation is only optimized for Linux/Codespaces.")

      # 2. Test if the server is already running
      try:
          requests.get(self.OLLAMA_URL, timeout=2)
          print("✅ Ollama server is already running.")
      except requests.exceptions.ConnectionError:
          print("⚠️ Ollama server is not running. Starting background process...")
          try:
              # Launch server in the background (detached stdout/stderr)
              subprocess.Popen(
                  ["ollama", "serve"], 
                  stdout=subprocess.DEVNULL, 
                  stderr=subprocess.DEVNULL,
                  start_new_session=True # Keeps the server alive after the script finishes
              )
              
              # 3. Poll until the server actively responds
              for _ in range(15):  # Try for up to 15 seconds
                  time.sleep(1)
                  try:
                      requests.get(self.OLLAMA_URL, timeout=1)
                      print("✅ Ollama server started successfully!")
                      return
                  except requests.exceptions.ConnectionError:
                      continue
              
              raise RuntimeError("Ollama server failed to respond within 15 seconds.")
          except Exception as e:
              raise RuntimeError(f"Failed to start Ollama server: {e}")
