import csv

def load_countries():
    with open('countries.csv', 'r', newline='') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header
        return [row for row in csv_reader]

def write_csv(data, filename):
    with open(filename, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(data[1:])

def main():
    csv_files = [
        'Annual_Surface_Temperature_Change.csv',
        'Climate-related_Disasters_Frequency.csv',
        'Forest_and_Carbon.csv',
        'Land_Cover_Accounts.csv'
    ]
    countries_data = load_countries()

    countries = [['ISO_Code', 'Display_Name', 'ISO', 'ISO3', 'FIPS', 'Region Name', 'Country_Status', 'Developed / Developing Countries', 'Population']]
    iso3_to_iso_code = {}  
    iso_code_counter = 895
    for row in countries_data:
        countries.append([row[2], row[4], row[0], row[1], row[3], row[12], row[17], row[18], row[23]])
        iso3_to_iso_code[row[1]] = row[2] if row[2] else str(iso_code_counter)
        if not row[2]:  # If ISO_Code is empty
            iso_code_counter += 1

    indicators = []
    measurements = []  
    measurements_data = []

    for csv_file in csv_files:
        with open(csv_file, 'r', newline='') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Skip header
            for row in csv_reader:
                iso3 = row[3]
                iso_code = iso3_to_iso_code.get(iso3, '')  
                if not iso_code:  # If ISO_Code is empty
                    iso_code = str(iso_code_counter)
                    iso3_to_iso_code[iso3] = iso_code  # Save the new ISO_Code for this ISO3
                    countries.append([iso_code, row[1], '', iso3, '', '', '', '', ''])  # Add new country to countries list
                    iso_code_counter += 1
                indicators_name = row[4]  
                unit = row[5] 
                climate_influence = row[10] if csv_file == 'Land_Cover_Accounts.csv' else '' 
                indicators_id = len(indicators)  
                indicators_row = [indicators_id, iso_code, indicators_name, unit, climate_influence] 
                years_data = {}
                for i in range(10, len(header)):  # Columns F1961 - F2022
                    year = header[i]
                    value = row[i] if row[i] != '' else None
                    years_data[year] = value
                measurements_data.append((indicators_id, iso_code, iso3, years_data))
                indicators.append(indicators_row)

    for indicators_id, iso_code, iso3, years_data in measurements_data:
        iso_code = iso3_to_iso_code.get(iso3, '') 
        measurement_id = len(measurements)  
        measurements_row = [measurement_id, indicators_id, iso_code, iso3] + [years_data.get(f'F{year}', '') for year in range(1961, 2023)] 
        measurements.append(measurements_row)

    write_csv(countries, 'out_countries.csv') 
    write_csv(indicators, 'indicators.csv')
    write_csv(measurements, 'measurements.csv')

if __name__ == "__main__":
    main()