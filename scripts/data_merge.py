import os
import pandas as pd
import geopandas as gpd

def load_and_merge_data():
    # Define base directory and subdirectories
<<<<<<< HEAD
    BASE_DIR = r"C:\Users\User\Desktop\project"
=======
    # Use relative path from the current working directory or project root
    BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
>>>>>>> de7e8fc3afaa07b13e2567664f434cb0e57d9c62
    ACS_DIR = os.path.join(BASE_DIR, "ACS Housing Data")
    TRACTS_DIR = os.path.join(BASE_DIR, "Census Tract Boundaries")
    HOLC_DIR = os.path.join(BASE_DIR, "HOLC Redlining Data")
    
    # Define file paths
    expected_files = {
        'age_sex': os.path.join(ACS_DIR, 'B01001_Age_Sex_2023.csv'),
        'race': os.path.join(ACS_DIR, 'B03002_Race_Ethnicity_2023.csv'),
        'years_occupied': os.path.join(ACS_DIR, 'B25037_Years_Occupied_2023.csv'),
        'rent_burden': os.path.join(ACS_DIR, 'B25070_Rent_Burden_2023.csv'),
        'home_values': os.path.join(ACS_DIR, 'B25082_Home_Values_2023.csv'),
        'mortgage_burden': os.path.join(ACS_DIR, 'B25091_Mortgage_Burden_2023.csv'),
        'poverty': os.path.join(ACS_DIR, 'S1701_Poverty_2023.csv'),
        'tracts': os.path.join(TRACTS_DIR, 'Census2020_Tracts_COA.geojson'),
        'holc': os.path.join(HOLC_DIR, 'HOLC_Atlanta_GA.geojson')
    }

    # Check for missing files
    missing_files = {k: v for k, v in expected_files.items() if not os.path.exists(v)}
    if missing_files:
        raise FileNotFoundError(f"Missing files: {missing_files}")

    # Load Census tract data
    print("⏳ Loading Census tract data...")
    tracts = gpd.read_file(expected_files['tracts'])
    print(f"Census tract columns: {tracts.columns.tolist()}")
    merged_data = tracts.copy()

    # Merge all ACS data
    print("⏳ Merging ACS data...")
    for key, filepath in expected_files.items():
        if key not in ['tracts', 'holc']:  # Skip GeoJSON files
            print(f"\nProcessing {key} data from {filepath}...")
            df = pd.read_csv(filepath)
            print(f"Original CSV columns: {df.columns.tolist()}")
            
            # Create standardized GEOID in both datasets
            if 'GEO_ID' in df.columns:
                df['GEOID'] = df['GEO_ID'].str.extract(r'US(\d+)$')
            
            # Drop duplicate columns before merge
            cols_to_drop = ['GEO_ID', 'NAME'] if 'GEO_ID' in df.columns else ['NAME']
            df = df.drop(columns=cols_to_drop, errors='ignore')
            print(f"CSV columns after cleanup: {df.columns.tolist()}")
            
            if 'GEOID' not in df.columns:
                raise ValueError(f"No GEOID column found in {key} data after processing")
            
            print(f"Merging on column: GEOID")
            merged_data = pd.merge(
                merged_data, 
                df, 
                on='GEOID', 
                how='left',
                suffixes=('', f'_{key}')  # Add dataset suffix to duplicate columns
<<<<<<< HEAD
            )

    # Load and merge HOLC data
    print("\n⏳ Merging HOLC redlining data...")
    holc = gpd.read_file(expected_files['holc'])
    final_data = gpd.sjoin(merged_data, holc, how='left', predicate='intersects')

    # Save results
    output_path = os.path.join(BASE_DIR, 'merged_housing_data.geojson')
=======
            )    # Load and merge HOLC data
    print("\n⏳ Merging HOLC redlining data...")
    holc = gpd.read_file(expected_files['holc'])
    
    # Ensure merged_data is still a GeoDataFrame
    if not isinstance(merged_data, gpd.GeoDataFrame):
        # Convert back to GeoDataFrame if it became a regular DataFrame
        merged_data = gpd.GeoDataFrame(merged_data, geometry=tracts.geometry)
    
    final_data = gpd.sjoin(merged_data, holc, how='left', predicate='intersects')    # Save results
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", 'merged_housing_data.geojson')
>>>>>>> de7e8fc3afaa07b13e2567664f434cb0e57d9c62
    final_data.to_file(output_path, driver='GeoJSON')
    print(f"\n✅ Data merged successfully! Saved to {output_path}")

if __name__ == "__main__":
    try:
        load_and_merge_data()
    except Exception as e:
        print(f"\n❌ Error in data processing: {str(e)}")
        raise