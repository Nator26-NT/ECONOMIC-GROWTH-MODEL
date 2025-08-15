import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class CurrencyStrengthAnalyzer:
    def __init__(self):
        self.exchange_rates = {
            'USD_ZAR': 18.5,  # 1 USD = 18.5 ZAR
            'CNY_ZAR': 2.55,  # 1 CNY = 2.55 ZAR
            'GBP_ZAR': 23.4,  # 1 GBP = 23.4 ZAR
        }
        
    def analyze_purchasing_power(self):
        """Analyze purchasing power parity across countries"""
        
        # Cost of living indices (New York = 100)
        ppp_data = {
            'Country': ['USA', 'China', 'England', 'South_Africa'],
            'Cost_Index': [100, 58, 127, 45],
            'Exchange_Rate_to_ZAR': [18.5, 2.55, 23.4, 1.0],
            'GDP_per_Capita_USD': [85000, 12500, 52000, 6800]
        }
        
        df = pd.DataFrame(ppp_data)
        
        # Calculate PPP-adjusted values
        df['PPP_Adjusted_Income'] = (df['GDP_per_Capita_USD'] * 100) / df['Cost_Index']
        df['Currency_Fair_Value'] = df['Exchange_Rate_to_ZAR'] * (df['Cost_Index'] / 100)
        
        return df
    
    def create_currency_dashboard(self):
        """Create comprehensive currency strength dashboard"""
        
        # Historical exchange rate trends (simulated)
        months = pd.date_range('2023-01-01', '2024-12-31', freq='M')
        
        currency_data = pd.DataFrame({
            'Date': months,
            'USD_ZAR': 18.5 + np.random.normal(0, 0.5, len(months)),
            'CNY_ZAR': 2.55 + np.random.normal(0, 0.1, len(months)),
            'GBP_ZAR': 23.4 + np.random.normal(0, 0.8, len(months))
        })
        
        # Calculate volatility
        volatility = {
            'USD': currency_data['USD_ZAR'].std(),
            'CNY': currency_data['CNY_ZAR'].std(),
            'GBP': currency_data['GBP_ZAR'].std()
        }
        
        return currency_data, volatility
    
    def generate_currency_report(self):
        """Generate comprehensive currency strength report"""
        
        ppp_analysis = self.analyze_purchasing_power()
        currency_data, volatility = self.create_currency_dashboard()
        
        # Currency strength ranking
        strength_ranking = ppp_analysis.sort_values('PPP_Adjusted_Income', ascending=False)
        
        return {
            'ppp_analysis': ppp_analysis,
            'currency_trends': currency_data,
            'volatility': volatility,
            'strength_ranking': strength_ranking
        }

# Generate currency analysis
analyzer = CurrencyStrengthAnalyzer()
currency_results = analyzer.generate_currency_report()

print("=== CURRENCY STRENGTH ANALYSIS ===")
print("\nPPP-Adjusted Income Ranking:")
print(currency_results['strength_ranking'][['Country', 'PPP_Adjusted_Income']])
print("\nCurrency Volatility (Standard Deviation):")
for currency, vol in currency_results['volatility'].items():
    print(f"{currency}: {vol:.3f}")

# Create visualization
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# PPP Comparison
ppp_data = currency_results['ppp_analysis']
ax1.bar(ppp_data['Country'], ppp_data['PPP_Adjusted_Income'])
ax1.set_title('PPP-Adjusted Income Comparison')
ax1.set_ylabel('PPP-Adjusted Income (USD)')
ax1.tick_params(axis='x', rotation=45)

# Currency Trends
currency_trends = currency_results['currency_trends']
ax2.plot(currency_trends['Date'], currency_trends['USD_ZAR'], label='USD/ZAR', linewidth=2)
ax2.plot(currency_trends['Date'], currency_trends['CNY_ZAR'], label='CNY/ZAR', linewidth=2)
ax2.plot(currency_trends['Date'], currency_trends['GBP_ZAR'], label='GBP/ZAR', linewidth=2)
ax2.set_title('Currency Exchange Rate Trends')
ax2.set_ylabel('Exchange Rate (ZAR)')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.savefig('currency_analysis.png', dpi=300, bbox_inches='tight')
plt.show()
