import pandas as pd
from datetime import datetime


def load_data():
    """
    Load and clean the health data from a CSV file.
    - Fill missing values in 'Steps' with the median value.
    - Fill missing values in 'Sleep_Hours' with 7.0.
    - Fill missing values in 'Heart_Rate_bpm' with 68.
    - Fill missing values in other columns with their respective median values.
    - Convert the 'Date' column to datetime objects.
    
    Returns:
        pd.DataFrame: Cleaned health data.
    """
    # Load data into a DataFrame
    df = pd.read_csv('data/health_data.csv')
    
    # Fill missing values in Steps with the median value of the column
    df['Steps'].fillna(df['Steps'].median(), inplace=True)
    
    # Fill missing values in Sleep_Hours with a default value of 7.0
    df['Sleep_Hours'].fillna(7.0, inplace=True)
    
    # Fill missing values in Heart_Rate_bpm with a default value of 68
    df['Heart_Rate_bpm'].fillna(68, inplace=True)
    
    # Convert 'Date' column to datetime objects
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    # Fill missing dates with sequential dates based on date range
    first_date = df['Date'].min()
    last_date = df['Date'].max()
    
    # Generate a complete daily date range
    date_range = pd.date_range(start=first_date, end=last_date, freq='D')
    df_complete = pd.DataFrame({'Date': date_range})
    
    # Merge with original data - missing dates will have NaN values for other columns
    df = df_complete.merge(df, on='Date', how='left')
    
    # For other columns not specifically addressed, fill missing values with the median
    for column in df.columns:
        if column not in ['Steps', 'Sleep_Hours', 'Heart_Rate_bpm', 'Date'] and df[column].isnull().any():
            df[column].fillna(df[column].median(), inplace=True)
    
    # Fill remaining missing values in the main columns
    df['Steps'].fillna(df['Steps'].median(), inplace=True)
    df['Sleep_Hours'].fillna(7.0, inplace=True)
    df['Heart_Rate_bpm'].fillna(68, inplace=True)
    
    return df


def calculate_recovery_score(df):
    """
    Calculate and add a 'Recovery_score' column to the DataFrame, which represents the daily recovery score.
    The score is calculated based on Sleep_Hours, Heart_Rate_bpm, and Steps.

    Recovery score factors:
    - Good sleep (7+ hours) improves recovery score.
    - Poor sleep (<6 hours) reduces recovery score.
    - Lower heart rate improves recovery score.
    - Very high activity (high steps) may slightly reduce recovery due to strain.

    Recovery_score is adjusted to be between 0 and 100.

    Args:
        df (pd.DataFrame): The DataFrame containing health data.

    Returns:
        pd.DataFrame: DataFrame with the new 'Recovery_score' column.
    """
    def clamp(value, min_value=0, max_value=100):
        """Ensure the recovery score remains within 0 to 100."""
        return max(min_value, min(value, max_value))

    # Define constants for calculation
    SCORE_SLEEP_GOOD = 20  # Increment for good sleep
    SCORE_SLEEP_BAD = 30  # Decrement for poor sleep
    SCORE_HEART_RATE_FACTOR = 0.5  # Factor to reduce score by heart rate
    SCORE_STEPS_LOW_ACTIVITY_PENALTY = 10
    SCORE_STEPS_HIGH_ACTIVITY_PENALTY = 15  # Factor to reduce score by steps over 12,000

    # Initialize the Recovery_score column
    df['Recovery_score'] = 50  # Start with a base score

    # Adjust score based on Sleep_Hours
    df.loc[df['Sleep_Hours'] >= 7, 'Recovery_score'] += SCORE_SLEEP_GOOD
    df.loc[df['Sleep_Hours'] < 6, 'Recovery_score'] -= SCORE_SLEEP_BAD

    # Adjust score based on Heart_Rate_bpm (lower is better)
    df['Recovery_score'] += (68 - df['Heart_Rate_bpm']) * SCORE_HEART_RATE_FACTOR

    # Adjust score based on Steps (very high levels might cause strain)
    df.loc[df['Steps'] < 4000, 'Recovery_score'] -= SCORE_STEPS_HIGH_ACTIVITY_PENALTY
    df.loc[df['Steps'] > 12000, 'Recovery_score'] -= SCORE_STEPS_HIGH_ACTIVITY_PENALTY

    # Ensure Recovery_score is between 0 and 100
    df['Recovery_score'] = df['Recovery_score'].apply(clamp)

    return df


def process_data():
    """
    Main function to process health data for the Streamlit dashboard.
    - Loads and cleans the data using load_data()
    - Calculates the Recovery Score using calculate_recovery_score()
    
    Returns:
        pd.DataFrame: Fully processed DataFrame with cleaned data and Recovery Score.
    """
    # Load and clean the data
    df = load_data()
    
    # Calculate and add the Recovery Score
    df = calculate_recovery_score(df)
    
    return df
