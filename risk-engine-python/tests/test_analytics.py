import pandas as pd
import numpy as np
from src.indicators import add_technical_indicators

def test_indicators_calculation():
    # Create dummy data
    data = {
        'Close': np.linspace(100, 200, 100),
        'Open': np.linspace(100, 200, 100),
        'High': np.linspace(110, 210, 100),
        'Low': np.linspace(90, 190, 100),
        'Volume': [1000] * 100
    }
    df = pd.DataFrame(data)
    
    # Process
    df_result = add_technical_indicators(df)
    
    # Assertions
    assert 'RSI' in df_result.columns
    assert 'SMA_20' in df_result.columns
    assert not df_result['RSI'].isnull().all()
    print("Test passed: Indicators calculated correctly.")
