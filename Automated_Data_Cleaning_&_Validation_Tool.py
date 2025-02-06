import pandas as pd
import numpy as np
import argparse
import json

# Function to clean dataset
def clean_data(file_path, output_path):
    df = pd.read_csv(file_path)
    report = {}
    
    # Handle missing values
    report['missing_values_before'] = df.isnull().sum().to_dict()
    df.fillna(method='ffill', inplace=True)
    report['missing_values_after'] = df.isnull().sum().to_dict()
    
    # Remove duplicates
    report['duplicates_before'] = df.duplicated().sum()
    df.drop_duplicates(inplace=True)
    report['duplicates_after'] = df.duplicated().sum()
    
    # Standardize text columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip().str.lower()
    
    # Detect outliers using IQR
    outlier_cols = df.select_dtypes(include=['number']).columns
    Q1 = df[outlier_cols].quantile(0.25)
    Q3 = df[outlier_cols].quantile(0.75)
    IQR = Q3 - Q1
    outliers = ((df[outlier_cols] < (Q1 - 1.5 * IQR)) | (df[outlier_cols] > (Q3 + 1.5 * IQR))).sum()
    report['outliers_detected'] = outliers.to_dict()
    
    # Save cleaned file
    df.to_csv(output_path, index=False)
    
    # Save report
    with open('cleaning_report.json', 'w') as f:
        json.dump(report, f, indent=4)
    
    print("Data cleaning complete. Summary report saved as cleaning_report.json")

# Command-line interface for execution
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Automated Data Cleaning Tool')
    parser.add_argument('input_file', type=str, help='Path to the input CSV file')
    parser.add_argument('output_file', type=str, help='Path to save the cleaned CSV file')
    args = parser.parse_args()
    clean_data(args.input_file, args.output_file)