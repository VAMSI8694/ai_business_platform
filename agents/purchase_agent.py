from agents.base_agent import BaseAgent

PURCHASE_SYSTEM_PROMPT = """
You are an expert AI Procurement & Purchase Agent for a business management platform.

Your responsibilities:
- Manage and optimize the purchasing process
- Evaluate and compare supplier quotes
- Track purchase orders and delivery schedules
- Negotiate better terms and pricing strategies
- Monitor inventory levels and trigger reorders
- Analyze spend patterns and identify savings
- Vendor performance management
- Contract management and compliance

When handling purchase decisions:
- Always compare multiple supplier options
- Calculate total cost of ownership (TCO)
- Evaluate quality, price, and delivery reliability
- Identify bulk purchase opportunities
- Flag single-source dependencies as risks
- Monitor payment terms and cash flow impact
- Track vendor scorecards

Be strategic, cost-conscious, and focused on supply chain resilience.
"""

class PurchaseAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="PurchaseAgent",
            system_prompt=PURCHASE_SYSTEM_PROMPT
        )
    
    def evaluate_purchase_order(self, po_data: dict) -> dict:
        """Evaluate a purchase order"""
        prompt = f"""
        Evaluate this purchase order:
        {po_data}
        
        Provide:
        1. Price competitiveness analysis
        2. Supplier reliability assessment
        3. Approval recommendation (approve/negotiate/reject)
        4. Alternative suppliers to consider
        5. Negotiation points if applicable
        """
        return self.chat(prompt, context=po_data)
    
    def analyze_vendor_performance(self, vendor_data: dict) -> dict:
        """Analyze vendor performance"""
        prompt = f"""
        Analyze vendor performance based on this data:
        {vendor_data}
        
        Provide:
        1. Overall vendor score (1-10)
        2. On-time delivery rate
        3. Quality rating
        4. Price competitiveness
        5. Recommendation (continue/renegotiate/replace)
        """
        return self.chat(prompt, context=vendor_data)
    
    def inventory_reorder_analysis(self, inventory_data: dict) -> dict:
        """Analyze inventory and recommend reorders"""
        prompt = f"""
        Analyze inventory levels and recommend reorder actions:
        {inventory_data}
        
        Provide:
        1. Items below reorder point
        2. Recommended order quantities (EOQ)
        3. Priority items (critical/normal/can wait)
        4. Estimated costs
        5. Suggested suppliers
        """
        return self.chat(prompt, context=inventory_data)
