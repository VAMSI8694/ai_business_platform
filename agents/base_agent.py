from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv()

class BaseAgent:
    def __init__(self, agent_name: str, system_prompt: str):
        self.agent_name = agent_name
        self.system_prompt = system_prompt
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
        self.conversation_history = []

    def chat(self, user_message: str, context: dict = None) -> dict:
        """Send message to OpenAI and get response"""
        
        # Build messages
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add context if provided
        if context:
            context_msg = f"Current business context:\n{json.dumps(context, indent=2)}"
            messages.append({"role": "user", "content": context_msg})
            messages.append({"role": "assistant", "content": "I have received the business context. How can I help you?"})
        
        # Add conversation history (last 10 messages)
        messages.extend(self.conversation_history[-10:])
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            assistant_message = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            return {
                "response": assistant_message,
                "tokens_used": tokens_used,
                "success": True,
                "agent_name": self.agent_name,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "response": f"Agent error: {str(e)}",
                "tokens_used": 0,
                "success": False,
                "agent_name": self.agent_name,
                "timestamp": datetime.utcnow().isoformat()
            }

    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []

    def get_structured_response(self, user_message: str, output_schema: dict) -> dict:
        """Get JSON structured response from agent"""
        schema_prompt = f"\nRespond ONLY with valid JSON matching this schema: {json.dumps(output_schema)}"
        result = self.chat(user_message + schema_prompt)
        
        try:
            result["structured_data"] = json.loads(result["response"])
        except json.JSONDecodeError:
            result["structured_data"] = None
            
        return result
