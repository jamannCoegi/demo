import os
import requests
import pandas as pd

# Retrieve the Census API key from environment variables
api_key = os.environ.get("CENSUS_TOKEN")

# URL for the Census API request
base_url = "https://api.census.gov/data/2020/acs/acs5"

# Define the variables for the data you want to pull
params = {
    "get": "B01003_001E,"  # Total population
           "B01001_002E,"  # Male population
           "B01001_026E,"  # Female population
           "B02001_002E,"  # White alone
           "B02001_003E,"  # Black or African American alone
           "B02001_005E,"  # Asian alone
           "B03002_012E,"  # Hispanic or Latino origin
           "B19013_001E,"  # Median household income
           "B15003_022E,"  # Bachelor's degree
           "B15003_023E,"  # Master's degree
           "B15003_024E,"  # Professional school degree
           "B15003_025E,"  # Doctorate degree
           "B27011_005E,"  # Employed with private health insurance
           "B992707_001E," # Total estimate for Medicaid/means-tested public coverage
           "B25077_001E,"  # Median home value
           "B19083_001E,"  # Gini index of income inequality
           "B15002_001E",  # Population over 25 years old
    "for": "zip code tabulation area:*",  # All ZIP codes
    "key": api_key
}

# Make the request to the Census API
response = requests.get(base_url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Convert the response to JSON
    data = response.json()

    # Convert the JSON data to a Pandas DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])
    df.columns = [
        "Total_Population",
        "Male_Population",
        "Female_Population",
        "White_Alone",
        "Black_Or_African_American_Alone",
        "Asian_Alone",
        "Hispanic_Or_Latino_Origin",
        "Median_Household_Income",
        "Bachelors_Degree",
        "Masters_Degree",
        "Professional_Degree",
        "Doctorate_Degree",
        "Employed_With_Private_Health_Insurance",
        "Medicaid_Or_Means_Tested_Public_Coverage",
        "Median_Home_Value",
        "Gini_Index",
        "Population_Over_25",
        "ZIP_Code"
    ]

    # Combine the columns for Master's, Professional, and Doctorate degrees
    df["Advanced_Degree"] = df[["Masters_Degree", "Professional_Degree", "Doctorate_Degree"]].apply(pd.to_numeric).sum(axis=1)

    # Drop the individual columns for Master's, Professional, and Doctorate degrees
    df.drop(columns=["Masters_Degree", "Professional_Degree", "Doctorate_Degree"], inplace=True)

    # Move the ZIP_Code column to the first position
    df = df[["ZIP_Code"] + [col for col in df.columns if col != "ZIP_Code"]]

    # Display the first few rows of the data
    print(df.head())

    # Optionally, save the DataFrame to a CSV file
    df.to_csv("zipcode_population_demographics_health_education.csv", index=False)
else:
    print(f"Error: {response.status_code} - {response.text}")
