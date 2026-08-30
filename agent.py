#Agent class
import os
from libs import Config
from libs import MyLogger
import sys
from libs import FreeModel

class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.key=Config.GEMINI_API_KEY
        self.logger=MyLogger(outputstream=sys.stdout)  # Initialize MyLogger with sys.stdout
        self.model=FreeModel().getModel(modelname="google")  # Default to Google model for now

    def perform_action(self):
        self.logger.info(f"{self.name} is performing their role as a {self.role}.")
        resp=self.model.invoke("Hello, tell me about the jupiter in 3 lines?")  # Example invocation of the model
        self.logger.info(f"Model response: {resp.content[0]['text']}")  # Log the model's response

if __name__ == "__main__":
    agent = Agent("Alice", "Data Analyst")
    agent.perform_action()  