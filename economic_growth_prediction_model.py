import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class SouthAfricaEconomicPredictor:
    def __init__(self):
        self.private_data = None
        self.public_data = None
        self.employment_predictions = None
        self.economic_model = None
        self.scaler = StandardScaler()
        
    def load_data(self):
        """Load all three CSV files"""
        self.private_data = pd.read_csv('south_africa_private_sector_growth.csv')
        self.public_data = pd.read_csv('south_africa_public_sector_growth.csv')
        self.employment_predictions = pd.read_csv('employment_growth_predictions.csv')
        
    def calculate_economic_indicators(self):
        """Calculate comprehensive economic indicators"""
        
        # Private sector economic contribution
        private_gdp = {
            'Finance': 0.25,  # 25% of GDP
            'ICT': 0.15,
            'Manufacturing': 0.12,
            'Construction': 0.08,
            'Agriculture': 0.05,
            'Transport': 0.06,
            'Wholesale': 0.10,
            'Other': 0.19
        }
        
        # Calculate weighted economic growth
        self.private_data['Economic_Contribution'] = self.private_data['Sector'].map(private_gdp)
        self.private_data['GDP_Impact'] = (self.private_data['Growth_%'] / 100) * self.private_data['Economic_Contribution']
        
        # Public sector contribution (government services)
        self.public_data['Economic_Contribution'] = 0.20  # 20% of GDP
        self.public_data['GDP_Impact'] = (self.public_data['Growth_%'] / 100) * self.public_data['Economic_Contribution']
        
    def predict_gdp_growth(self):
        """Predict GDP growth based on employment trends"""
        
        # Calculate base GDP from employment trends
        total_private_employment = self.private_data['Employment_2024'].sum()
        total_public_employment = self.public_data['Employment_2023'].sum()
        
        # Employment-based GDP estimation
        base_gdp = (total_private_employment * 85000 + total_public_employment * 75000) / 1e6  # In billions
        
        # Growth rate calculation
        private_growth = (self.private_data['GDP_Impact'] * self.private_data['Employment_2024']).sum() / total_private_employment
        public_growth = (self.public_data['GDP_Impact'] * self.public_data['Employment_2023']).sum() / total_public_employment
        
        # Weighted average growth
        total_growth = (private_growth * 0.8 + public_growth * 0.2) * 100
        
        return {
            'base_gdp_billion': base_gdp,
            'predicted_growth_rate': total_growth,
            'gdp_2024': base_gdp * (1 + total_growth/100)
        }
    
    def create_international_comparison(self):
        """Create comparison framework with USA, China, England"""
        
        # 2024 Economic data (in trillions USD)
        countries = {
            'USA': {'gdp': 28.0, 'employment_millions': 160, 'currency_strength': 1.0},
            'China': {'gdp': 18.0, 'employment_millions': 780, 'currency_strength': 0.14},
            'England': {'gdp': 3.5, 'employment_millions': 33, 'currency_strength': 1.27},
            'South_Africa': {'gdp': 0.4, 'employment_millions': 16.5, 'currency_strength': 0.053}
        }
        
        # Normalize metrics (0-100 scale)
        comparison_df = pd.DataFrame(countries).T
        
        # Economic size index
        comparison_df['Economic_Size_Index'] = (comparison_df['gdp'] / comparison_df['gdp'].max()) * 100
        
        # Employment market strength
        comparison_df['Employment_Strength'] = (comparison_df['employment_millions'] / comparison_df['employment_millions'].max()) * 100
        
        # Currency strength
        comparison_df['Currency_Power'] = (comparison_df['currency_strength'] / comparison_df['currency_strength'].max()) * 100
        
        # Composite power index
        comparison_df['Composite_Power'] = (
            comparison_df['Economic_Size_Index'] * 0.4 +
            comparison_df['Employment_Strength'] * 0.3 +
            comparison_df['Currency_Power'] * 0.3
        )
        
        return comparison_df
    
    def generate_predictions(self):
        """Generate comprehensive economic predictions"""
        
        self.load_data()
        self.calculate_economic_indicators()
        
        # GDP predictions
        gdp_forecast = self.predict_gdp_growth()
        
        # International comparison
        comparison = self.create_international_comparison()
        
        # Employment predictions extension
        employment_2028 = self.employment_predictions[
            self.employment_predictions['Year'] == 2028
        ]['Predicted_Employment'].sum()
        
        return {
            'gdp_forecast': gdp_forecast,
            'international_comparison': comparison,
            'employment_2028': employment_2028,
            'economic_ranking': comparison.sort_values('Composite_Power', ascending=False)
        }

# Initialize and run predictions
predictor = SouthAfricaEconomicPredictor()
results = predictor.generate_predictions()

print("=== SOUTH AFRICA ECONOMIC GROWTH PREDICTIONS ===")
print(f"Predicted GDP 2024: ${results['gdp_forecast']['gdp_2024']:.2f} billion")
print(f"Growth Rate: {results['gdp_forecast']['predicted_growth_rate']:.2f}%")
print(f"\n=== INTERNATIONAL COMPARISON (2024) ===")
print(results['economic_ranking'][['Composite_Power', 'Economic_Size_Index', 'Currency_Power']])
