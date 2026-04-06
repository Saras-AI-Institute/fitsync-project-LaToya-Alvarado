import pandas as pd

def main():
    # Load the CSV file into a DataFrame
    df = pd.read_csv('data/health_data.csv')
    
    # Display the first 5 rows
    print("First 5 rows:")
    print(df.head())
    
    # Calculate the number of missing values in each column
    missing_values = df.isnull().sum()
    print("\nNumber of missing values in each column:")
    print(missing_values)

if __name__ == "__main__":
    main()