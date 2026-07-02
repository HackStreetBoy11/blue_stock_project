# recommender.py
import pandas as pd
import os

def recommend_funds(risk_appetite):
    # Handle paths fluidly
    file_path = 'data/fund_scorecard.csv'
    if not os.path.exists(file_path) and os.path.exists('../data/fund_scorecard.csv'):
        file_path = '../data/fund_scorecard.csv'
        
    df_scorecard = pd.read_csv(file_path)
    
    # Standardize input string
    risk_appetite = risk_appetite.strip().lower()
    
    # Dynamically assign a risk grade based on the 'beta' column in your data
    # Fall back to max_drawdown or final_score if beta has any issues
    if 'beta' in df_scorecard.columns:
        df_scorecard['computed_risk'] = pd.cut(
            df_scorecard['beta'], 
            bins=[-float('inf'), 0.8, 1.2, float('inf')], 
            labels=['low', 'moderate', 'high']
        )
    else:
        # Fallback approximation using final score distribution if beta isn't populated
        df_scorecard['computed_risk'] = pd.qcut(
            df_scorecard['final_score'], 
            q=3, 
            labels=['low', 'moderate', 'high']
        )

    # Filter by user preference
    filtered_funds = df_scorecard[df_scorecard['computed_risk'] == risk_appetite]
    
    if filtered_funds.empty:
        print(f"⚠️ No funds found matching risk profile '{risk_appetite}'.")
        return pd.DataFrame()

    # Sort to return top 3 performers by Sharpe Ratio
    top_3 = filtered_funds.sort_values(by='sharpe_ratio', ascending=False).head(3)
    
    # Return pristine, clean summary columns
    return top_3[['scheme_name', 'beta', 'sharpe_ratio', 'cagr_3yr', 'final_score']]

if __name__ == "__main__":
    user_input = input("Enter risk appetite (Low / Moderate / High): ").strip()
    if user_input.lower() in ['low', 'moderate', 'high']:
        recommendations = recommend_funds(user_input)
        if not recommendations.empty:
            print(f"\n--- Top 3 Recommended Funds for {user_input.capitalize()} Risk Appetite (Based on Beta Calibration) ---")
            print(recommendations.to_string(index=False))
    else:
        print("❌ Invalid input. Please enter Low, Moderate, or High.")