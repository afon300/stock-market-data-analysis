import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from datetime import timedelta

def predict_next_days(df, days_to_predict=7):
    """
    Predicts asset prices for a specified horizon using a Random Forest Regressor.
    
    DISCLAIMER: This model is for educational purposes only. Financial markets 
    are stochastic and influenced by numerous external factors that historical 
    price data alone cannot capture.
    
    Approach: Recursive multi-step forecasting using lagged price features.
    """
    # Feature Engineering: Use past 5 days as features
    data = df[['Close']].copy()
    for i in range(1, 6):
        data[f'Lag_{i}'] = data['Close'].shift(i)
    
    data = data.dropna()
    
    X = data.drop('Close', axis=1)
    y = data['Close']
    
    # Train the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X.values, y.values)
    
    # Recursive prediction for future days
    last_features = X.iloc[-1].values.reshape(1, -1)
    predictions = []
    
    current_features = last_features.copy()
    for _ in range(days_to_predict):
        pred = model.predict(current_features)[0]
        predictions.append(pred)
        
        # Update features for next prediction: [pred, lag1, lag2, lag3, lag4]
        current_features = np.roll(current_features, 1)
        current_features[0, 0] = pred
        
    # Create future dates
    last_date = df.index[-1]
    future_dates = [last_date + timedelta(days=i+1) for i in range(days_to_predict)]
    
    return pd.Series(predictions, index=future_dates)
