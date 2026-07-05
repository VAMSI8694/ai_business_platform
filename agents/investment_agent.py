from agents.base_agent import BaseAgent

INVESTMENT_SYSTEM_PROMPT = """
You are an expert AI Investment & Financial Planning Agent for a business management platform.

Your responsibilities:
- Analyze investment portfolios and performance
- Evaluate capital expenditure (CAPEX) decisions
- ROI analysis for business investments
- Risk assessment and portfolio diversification
- Cash flow forecasting for investment planning
- Working capital optimization
- Financial ratio analysis (ROE, ROA, ROIC)
- Merger & acquisition evaluation
- Strategic financial planning and budgeting

When analyzing investments:
- Calculate NPV, IRR, and payback period
- Assess risk-adjusted returns
- Compare investment alternatives
- Identify opportunity costs
- Monitor market conditions impact
- Evaluate liquidity and exit strategies
- Flag investments underperforming benchmarks

Be analytical, risk-aware, and focused on long-term value creation.
"""

class InvestmentAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="InvestmentAgent",
            system_prompt=INVESTMENT_SYSTEM_PROMPT
        )
    
    def analyze_investment_portfolio(self, portfolio_data: dict) -> dict:
        """Analyze investment portfolio"""
        prompt = f"""
        Analyze this investment portfolio:
        {portfolio_data}
        
        Provide:
        1. Portfolio performance summary
        2. Asset allocation analysis
        3. Top and bottom performers
        4. Risk assessment
        5. Rebalancing recommendations
        """
        return self.chat(prompt, context=portfolio_data)
    
    def evaluate_capex_decision(self, investment_proposal: dict) -> dict:
        """Evaluate a capital expenditure decision"""
        prompt = f"""
        Evaluate this CAPEX investment proposal:
        {investment_proposal}
        
        Provide:
        1. NPV calculation and interpretation
        2. IRR analysis
        3. Payback period
        4. Risk assessment (scale 1-10)
        5. Recommendation (approve/reject/modify) with reasoning
        """
        return self.chat(prompt, context=investment_proposal)
    
    def strategic_financial_plan(self, company_data: dict, horizon: str) -> dict:
        """Create strategic financial plan"""
        prompt = f"""
        Create a strategic financial plan for {horizon} based on:
        {company_data}
        
        Provide:
        1. Financial goals and targets
        2. Investment priorities
        3. Capital allocation strategy
        4. Risk mitigation plan
        5. Key milestones and metrics to track
        """
        return self.chat(prompt, context=company_data)
