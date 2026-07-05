from agents.base_agent import BaseAgent

ACCOUNTS_SYSTEM_PROMPT = """
You are an expert AI Accounts & Finance Agent for a business management platform.

Your responsibilities:
- Analyze financial statements, balance sheets, and P&L reports
- Track accounts receivable and payable
- Provide insights on cash flow and liquidity
- Identify financial risks and opportunities
- Generate financial summaries and forecasts
- Answer questions about transactions, invoices, and payments
- Suggest cost-cutting measures and budget optimizations

When analyzing data:
- Always provide specific numbers and percentages
- Highlight red flags (overdue payments, unusual expenses)
- Give actionable recommendations
- Use professional accounting terminology
- Format financial data clearly with proper labels

You have access to the company's accounting database including:
- All transactions and ledger entries
- Account balances and statements
- Invoice and payment records
- Budget allocations and actuals

Be precise, professional, and proactive in identifying financial insights.
"""

class AccountsAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="AccountsAgent",
            system_prompt=ACCOUNTS_SYSTEM_PROMPT
        )
    
    def analyze_financial_health(self, financial_data: dict) -> dict:
        """Analyze overall financial health"""
        prompt = f"""
        Analyze this financial data and provide a comprehensive health report:
        {financial_data}
        
        Include:
        1. Overall financial health score (1-10)
        2. Key strengths
        3. Critical issues
        4. Top 3 immediate action items
        5. 30-day forecast
        """
        return self.chat(prompt, context=financial_data)
    
    def process_invoice(self, invoice_data: dict) -> dict:
        """Process and analyze an invoice"""
        prompt = f"""
        Review this invoice and provide:
        1. Validation check (is everything correct?)
        2. Payment priority (urgent/normal/can wait)
        3. Any discrepancies or issues
        4. Recommended action
        
        Invoice: {invoice_data}
        """
        return self.chat(prompt)
    
    def generate_financial_report(self, period: str, data: dict) -> dict:
        """Generate a formatted financial report"""
        prompt = f"""
        Generate a professional financial report for {period}.
        
        Include:
        - Revenue summary
        - Expense breakdown
        - Net profit/loss
        - Key metrics (gross margin, operating ratio)
        - Month-over-month comparison
        - Recommendations
        
        Data: {data}
        """
        return self.chat(prompt, context=data)
