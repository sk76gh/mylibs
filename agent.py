#Agent class
import os
from config import Config
from mylogger import MyLogger
import sys

class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.key=Config.GEMINI_API_KEY
        self.logger=MyLogger(outputstream=sys.stdout)  # Initialize MyLogger with sys.stdout
        

    def perform_action(self):
        self.logger.info(f"{self.name} is performing their role as a {self.role}.")
   
           
        
if __name__ == "__main__":
    agent = Agent("Alice", "Data Analyst")
    agent.perform_action()  