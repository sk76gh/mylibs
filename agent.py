#Agent class
import os
from config import Config

class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.key=Config.OPENAI_API_KEY
        

    def perform_action(self):
        print(f"{self.name} is performing their role as a {self.role}.")
        print(f"Using API Key: {self.key}")    
        
if __name__ == "__main__":
    agent = Agent("Alice", "Data Analyst")
    agent.perform_action()  