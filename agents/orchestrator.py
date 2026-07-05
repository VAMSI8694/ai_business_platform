from openai import OpenAI
from agents.accounts_agent import AccountsAgent
from agents.sales_agent import SalesAgent
from agents.purchase_agent import PurchaseAgent
from agents.manufacturing_agent import ManufacturingAgent
from agents.investment_agent import InvestmentAgent
from dotenv import load_dotenv
import os
import json

load_dotenv()

class AgentOrchestrator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
        
        # Initialize all agents
        self.agents = {
            "accounts": AccountsAgent(),
            "manufacturing": ManufacturingAgent(),
            "purchase": PurchaseAgent(),
            "sales": SalesAgent(),
            "investment": InvestmentAgent()
        }
        
        self.agent_descriptions = {
            "accounts": "Handles finance, accounting, invoices, transactions, cash flow, P&L",
            "manufacturing": "Handles production, operations, machinery, work orders, quality control",
            "purchase": "Handles procurement, suppliers, purchase orders, inventory, vendor management",
            "sales": "Handles sales, revenue, customers, CRM, forecasting, pipeline",
            "investment": "Handles investments, CAPEX, ROI, portfolio, financial planning"
        }
    
    def route_to_agent(self, user_message: str) -> str:
        """Use GPT-4 to determine which agent should handle the request"""
        routing_prompt = f"""
        You are a routing system for a business AI platform.
        Determine which agent should handle this user request.
        
        Available agents:
        {json.dumps(self.agent_descriptions, indent=2)}
        
        User request: "{user_message}"
        
        Respond with ONLY the agent name (one of: accounts, manufacturing, purchase, sales, investment).
        If the request spans multiple domains, pick the most relevant one.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": routing_prompt}],
            temperature=0,
            max_tokens=20
        )
        
        agent_name = response.choices[0].message.content.strip().lower()
        
        # Validate the response
        if agent_name not in self.agents:
            # Default to accounts if routing fails
            agent_name = "accounts"
        
        return agent_name
    
    def process_request(self, user_message: str, agent_override: str = None, context: dict = None) -> dict:
        """Process a user request through the appropriate agent"""
        
        # Determine which agent to use
        if agent_override and agent_override in self.agents:
            agent_name = agent_override
            routing_reason = "Manual selection"
        else:
            agent_name = self.route_to_agent(user_message)
            routing_reason = "Auto-routed by orchestrator"
        
        # Get the agent
        agent = self.agents[agent_name]
        
        # Process the request
        result = agent.chat(user_message, context=context)
        
        # Add routing info
        result["routed_to"] = agent_name
        result["routing_reason"] = routing_reason
        
        return result
    
    def broadcast_to_all_agents(self, message: str, context: dict = None) -> dict:
        """Send a request to all agents and compile responses"""
        responses = {}
        
        for agent_name, agent in self.agents.items():
            result = agent.chat(message, context=context)
            responses[agent_name] = result
        
        # Compile summary using GPT-4
        summary_prompt = f"""
        Multiple AI business agents have analyzed the following request: "{message}"
        
        Their responses:
        {json.dumps({k: v['response'] for k, v in responses.items()}, indent=2)}
        
        Please provide a unified executive summary that combines the key insights from all agents.
        Format it as a structured report with sections for each business area.
        """
        
        summary_response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": summary_prompt}],
            temperature=0.7,
            max_tokens=3000
        )
        
        return {
            "individual_responses": responses,
            "executive_summary": summary_response.choices[0].message.content,
            "success": True
        }
    
    def reset_all_agents(self):
        """Reset conversation history for all agents"""
        for agent in self.agents.values():
            agent.reset_conversation()
    
    def get_agent(self, agent_name: str):
        """Get a specific agent by name"""
        return self.agents.get(agent_name)

# Global orchestrator instance
orchestrator = AgentOrchestrator()
