import geopandas as gpd
import pandas as pd
import random
import csv

def generate_random_data():
    """
    Generates random data for all municipalities in the Community of Madrid
    based on SHP files and saves them to a CSV file.
    """
    
    # Load the shapefile
    print("Loading municipality data...")
    gdf = gpd.read_file('boundaries/recintos_municipales_inspire_peninbal_etrs89.shp')
    
    # Filter only Madrid municipalities (ES30)
    madrid_municipalities = gdf[gdf['CODNUT2'] == 'ES30']
    
    print(f"Found {len(madrid_municipalities)} municipalities in Madrid")
    
    # List to store generated data
    municipalities_data = []
    
    # Generate random data for each municipality
    for idx, row in madrid_municipalities.iterrows():
        nameunit = row['NAMEUNIT']
        natcode = row['NATCODE']
        
        # Generate realistic random data
        # Population: between 1,000 and 500,000 inhabitants
        population = random.randint(1000, 500000)
        
        # Rent price: between 400 and 1200 euros/month
        rent = random.randint(400, 1200)
        
        # Maximum temperature: between 20 and 40 degrees Celsius
        maxtemp = random.randint(20, 40)
        
        # Accessibility scores (0-100)
        schools = random.randint(60, 100)
        pharmacies = random.randint(70, 100)
        hospitals = random.randint(50, 95)
        parks = random.randint(60, 95)
        cinemas = random.randint(30, 80)
        restaurants = random.randint(70, 100)
        supermarkets = random.randint(80, 100)
        
        # Add data to the list
        municipalities_data.append({
            'NAMEUNIT': nameunit,
            'NATCODE': natcode,
            'population': population,
            'rent': rent,
            'maxtemp': maxtemp,
            'schools': schools,
            'pharmacies': pharmacies,
            'hospitals': hospitals,
            'parks': parks,
            'cinemas': cinemas,
            'restaurants': restaurants,
            'supermarkets': supermarkets
        })
    
    # Create DataFrame
    df = pd.DataFrame(municipalities_data)
    
    # Save to CSV file
    output_file = 'municipalities.csv'
    df.to_csv(output_file, index=False)
    
    print(f"Data saved to {output_file}")
    print(f"Total municipalities processed: {len(df)}")
    
    # Show first rows as example
    print("\nFirst 5 rows of the dataset:")
    print(df.head().to_string(index=False))
    
    return df

if __name__ == "__main__":
    # Set seed for reproducibility (optional)
    random.seed(42)
    
    # Generate the data
    data = generate_random_data()
