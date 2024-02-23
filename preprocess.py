import pandas as pd
import time
import requests

def geocode_address(components):
    api_key = "AIzaSyC-OSR4XOBFf3zJCF8DThegIzu5hqQtChQ"  # Replace with your Google Maps API key
    url = f"https://maps.googleapis.com/maps/api/geocode/json?components={components}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    elif data['status'] == "ZERO_RESULTS" or data['status'] == "INVALID_REQUEST":
        return None, None
    else:
        print("Trying again for %s..."%components)
        print(data['status'])
        time.sleep(30)
        return geocode_address(components)

def geocode_city_country(city, country):
    components = "locality:"+ city.replace(" ", "+") + "|country:" + country
    return geocode_address(components)

def main():
    file_path = 'beer_with_locations.csv'
    df = pd.read_csv(file_path)

    df["Latitude"] = ""
    df["Longitude"] = ""

    for index, row in df.iterrows():
        try:
            city = row["City"]
            country = row["Country"]
            latitude, longitude = geocode_city_country(city, country)
            if latitude == None:
                df.drop(index, inplace=True)
            else:
                df.at[index, 'Latitude'] = latitude
                df.at[index, 'Longitude'] = longitude
        except IndexError:
            df.drop(index, inplace=True)
    
    df.to_csv(file_path)

if __name__ == "__main__":
    main()