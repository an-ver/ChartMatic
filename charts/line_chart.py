import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine
from flask import send_file

def generate_line_chart(country_names, indicator_names, aggr_value, start_year, end_year):

    engine = create_engine('mysql+pymysql://root:ROOT@localhost/my_dbms')

    # Load data
    measurements_df = pd.read_sql('SELECT * FROM measurements', engine)
    indicators_df = pd.read_sql('SELECT * FROM indicators', engine)
    countries_df = pd.read_sql('SELECT * FROM countries', engine)

    # Melt the measurements to DataFrame
    measurements_df = measurements_df.melt(id_vars=['Measurements_id', 'Indicators_id', 'ISO_Code', 'ISO3'], 
                                           var_name='Year', 
                                           value_name='Event Value')

    measurements_df['Year'] = measurements_df['Year'].str[1:].astype(int)

    aggr_value = int(aggr_value)
    start_year = int(start_year)
    end_year = int(end_year)
    plt.figure(figsize=(10, 6))

    all_years = [] 

    for country_name in country_names:
        data_available = True  # Reset flag to True at the beginning of indicator loop

        if country_name in countries_df['Display_Name'].values:
            country_iso_code = countries_df[countries_df['Display_Name'] == country_name]['ISO_Code'].values[0]
        else:
            print(f"Country name {country_name} not found in DataFrame.")
            data_available = False  # Set flag to False if country name is not found

        for indicator_name in indicator_names:
            if data_available: 
                indicator_df = indicators_df[(indicators_df['Indicators'] == indicator_name) & (indicators_df['ISO_Code'] == country_iso_code)]
                if not indicator_df.empty:
                    indicator_id = indicator_df['Indicators_id'].values[0]
                else:
                    print(f"Indicator name {indicator_name} not found for country {country_name} in DataFrame.")
                    continue  # Skip to next indicator if current indicator is not found

                merged_df = pd.merge(measurements_df, indicators_df, on=['ISO_Code', 'Indicators_id'])
                merged_df = pd.merge(merged_df, countries_df, on='ISO_Code')
                merged_df = merged_df[merged_df['Event Value'] != 0]

                country_data = merged_df[(merged_df['ISO_Code'] == country_iso_code) & (merged_df['Indicators_id'] == indicator_id)]
                
                # Filter the data based on the start and end year
                country_data = country_data[(country_data['Year'] >= start_year) & (country_data['Year'] <= end_year)]
                
                country_data[f'Year_{aggr_value}'] = (country_data['Year'] // aggr_value) * aggr_value
                
                country_data_grouped = country_data.groupby(f'Year_{aggr_value}')['Event Value'].mean().reset_index()

                years = country_data_grouped[f'Year_{aggr_value}'].unique()
                all_years.extend(years) 

                if not country_data_grouped.empty:
                    plt.plot(country_data_grouped['Event Value'], label=f'Country {country_name} Indicator {indicator_name}')
                else:
                    print(f"No data available for Country {country_name} and Indicator {indicator_name}")
                    data_available = False 
        
    plt.title(f'Line Chart ({aggr_value}-Year Aggregation)')
    plt.xlabel('Year')
    plt.ylabel('indicators Events')
    plt.grid(True) 
    plt.legend(prop={'size': 6}, loc='upper left')
    plt.xticks(np.arange(len(np.unique(all_years))), np.unique(all_years), rotation='vertical')
    
    image_dir = 'images/'
    os.makedirs(image_dir, exist_ok=True)

    plt.savefig(os.path.join(image_dir, 'line_chart.png'))

    # Return the path to the image file
    return send_file(os.path.join('images', 'line_chart.png'), mimetype='image/png')