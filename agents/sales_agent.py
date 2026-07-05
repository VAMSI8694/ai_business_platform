from agents.base_agent import BaseAgent

SALES_SYSTEM_PROMPT = """
You are an expert AI Sales & Revenue Agent for a business management platform.

Your responsibilities:
- Analyze sales performance and pipeline
- Track customer relationships and interactions
- Forecast revenue and sales trends
- Identify upselling and cross-selling opportunities
- Monitor sales team performance and KPIs
- Customer segmentation and targeting
- Pricing strategy optimization
- Sales funnel analysis and conversion rates
- Churn prediction and retention strategies

When analyzing sales data:
- Calculate key metrics: conversion rate, ACV, LTV, CAC
- Identify top and bottom performing products/regions
- Spot seasonal trends and patterns
- Flag at-risk customers (low engagement, overdue payments)
- Recommend targeted campaigns
- Analyze win/loss reasons
- Benchmark against targets and quotas

Be data-driven, customer-focused, and growth-oriented.
"""

class SalesAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_name="SalesAgent",
            system_prompt=SALES_SYSTEM_PROMPT
        )
    
    def analyze_sales_performance(self, sales_data: dict) -> dict:
        """Analyze sales performance"""
        prompt = f"""
        Analyze this sales performance data:
        {sales_data}
        
        Provide:
        1. Revenue vs target analysis
        2. Top performing products/services
        3. Underperforming areas
        4. Customer acquisition trends
        5. Top 5 actionable recommendations
        """
        return self.chat(prompt, context=sales_data)
    
    def forecast_revenue(self, historical_data: dict, period: str) -> dict:
        """Forecast revenue for a period"""
        prompt = f"""
        Based on historical data, forecast revenue for {period}:
        {historical_data}
        
        Provide:
        1. Revenue forecast (optimistic/realistic/pessimistic)
        2. Key growth drivers
        3. Risk factors
        4. Confidence level
        5. Recommended actions to hit targets
        """
        return self.chat(prompt, context=historical_data)
    
    def customer_insights(self, customer_data: dict) -> dict:
        """Generate customer insights"""
        prompt = f"""
        Analyze customer data and provide insights:
        {customer_data}
        
        Provide:
        1. Customer segmentation
        2. High-value customer profiles
        3. At-risk customers
        4. Upsell/cross-sell opportunities
        5. Retention strategies
        """
        return self.chat(prompt, context=customer_data)
