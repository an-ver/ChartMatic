import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import os
from flask import send_file

def generate_scatter_plot(country, indicators):

    # Create engine
    engine = create_engine('mysql+pymysql://root:ROOT@localhost/my_dbms')

    # Load data
    measurements_df = pd.read_sql('SELECT * FROM measurements', engine)
    indicators_df = pd.read_sql('SELECT * FROM indicators', engine)
    countries_df = pd.read_sql('SELECT * FROM countries', engine)

    # Melt the measurements DataFrame
    measurements_df = measurements_df.melt(id_vars=['Measurements_id', 'Indicators_id', 'ISO_Code', 'ISO3'], 
                                           var_name='Year', 
                                           value_name='Event Value')
    measurements_df['Year'] = measurements_df['Year'].str[1:].astype(int)


    plt.figure(figsize=(10, 5))

    # Check if the country exists
    if country in countries_df['Display_Name'].values:
        country_iso_code = countries_df[countries_df['Display_Name'] == country]['ISO_Code'].values[0]

    # Initialize empty lists to store data for each indicator
    indicator_ids = []
    indicator_data = []

    # Loop over each indicator
    for indicator in indicators:
        # Translate indicator names to IDs
        indicator_df = indicators_df[(indicators_df['Indicators'] == indicator) & (indicators_df['ISO_Code'] == country_iso_code)]
        if not indicator_df.empty:
            indicator_id = indicator_df['Indicators_id'].values[0]
            indicator_ids.append(indicator_id)
        else:
            print(f"Indicator name {indicator} not found for country {country} in DataFrame.")
            continue  # Skip to next indicator if current indicator is not found

        # Filter measurements for the selected country and indicator
        indicator_data_df = measurements_df[(measurements_df['ISO_Code'] == country_iso_code) & (measurements_df['Indicators_id'] == indicator_id)]
        indicator_data_df['Year'] = indicator_data_df['Year'].astype(int)
        indicator_data.append(indicator_data_df)
        # Sort indicator_data by the order of indicators
    
    indicator_data = [x for _, x in sorted(zip(indicators, indicator_data))]


    # Check if data was found for both indicators
    if len(indicator_data) == 2 and len(indicator_ids) == 2:
        # Merge the two dataframes on 'Year'
        merged_df = pd.merge(indicator_data[0], indicator_data[1], on='Year', suffixes=('_ind1', '_ind2'))
        merged_df = merged_df[(merged_df['Event Value_ind1'] != 0) & (merged_df['Event Value_ind2'] != 0)]

        # Plot the scatter plot
        plt.scatter(merged_df['Event Value_ind1'], merged_df['Event Value_ind2'])
        plt.title(f'Scatter Plot of {indicators[0]} vs {indicators[1]} for {country}', fontsize=7)  
        plt.xlabel(indicators[0])
        plt.ylabel(indicators[1])
        plt.grid(True)
        plt.subplots_adjust(bottom=0.2)
        plt.tight_layout()
    else:
        plt.title("No data available for the selected countries and indicators.")
        plt.xlabel(indicators[0])
        plt.ylabel(indicators[1])
        plt.grid(True)
    
    image_dir = 'images/'
    os.makedirs(image_dir, exist_ok=True)

    plt.savefig(os.path.join(image_dir, 'scatter_plot.png'))

    return send_file(os.path.join('images', 'scatter_plot.png'), mimetype='image/png')