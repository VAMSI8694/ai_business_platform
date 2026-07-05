from agents.base_agent import BaseAgent

MANUFACTURING_SYSTEM_PROMPT = """
You are an expert AI Manufacturing & Operations Agent for a business management platform.

Your responsibilities:
- Monitor and optimize production schedules
- Track work-in-progress (WIP) and finished goods
- Analyze machine utilization and downtime
- Manage Bill of Materials (BOM) and routing
- Identify production bottlenecks and inefficiencies
- Quality control monitoring and defect analysis
- Capacity planning and resource allocation
- Maintenance scheduling and predictive maintenance
- Supply chain coordination for raw materials

When analyzing manufacturing data:
- Calculate OEE (Overall Equipment Effectiveness)
- Identify bottlenecks in production flow
- Suggest lean manufacturing improvements
- Monitor KPIs: cycle time, throughput, scrap rate
- Flag critical equipment that needs attention
- Forecast production completion times

Be analytical, precise, and focused on operational efficiency.
"""

class ManufacturingAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="ManufacturingAgent",
            system_prompt=MANUFACTURING_SYSTEM_PROMPT
        )
    
    def analyze_production_order(self, order_data: dict) -> dict:
        """Analyze a manufacturing order"""
        prompt = f"""
        Analyze this manufacturing order:
        {order_data}
        
        Provide:
        1. Feasibility assessment
        2. Resource requirements
        3. Estimated completion time
        4. Potential risks/bottlenecks
        5. Optimization recommendations
        """
        return self.chat(prompt, context=order_data)
    
    def optimize_production_schedule(self, orders: list, resources: dict) -> dict:
        """Optimize production scheduling"""
        prompt = f"""
        Optimize the production schedule for these orders given available resources.
        
        Orders: {orders}
        Available Resources: {resources}
        
        Provide:
        1. Recommended production sequence
        2. Resource allocation plan
        3. Expected completion dates
        4. Utilization percentages
        5. Risk mitigation strategies
        """
        return self.chat(prompt)
    
    def quality_analysis(self, quality_data: dict) -> dict:
        """Analyze quality control data"""
        prompt = f"""
        Analyze quality control data and identify issues:
        {quality_data}
        
        Provide:
        1. Defect rate analysis
        2. Root cause identification
        3. Affected batches/products
        4. Corrective actions
        5. Preventive measures
        """
        return self.chat(prompt, context=quality_data)
