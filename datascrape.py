from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import common
import pandas as pd
import re

class Cache:
    def __init__(self, max_size):
        self.cache = {}
        self.max_size = max_size

    def get(self, key):
        if key in self.cache:
            # If the key exists, return the value and move the key to the end (most recently used)
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        else:
            return None

    def set(self, key, value):
        if len(self.cache) >= self.max_size:
            # If the cache is full, remove the least recently used item (first item in dictionary)
            self.cache.pop(next(iter(self.cache)))
        self.cache[key] = value

    def remove(self, key):
        if key in self.cache:
            del self.cache[key]

    def clear(self):
        self.cache.clear()

    def __repr__(self):
        return repr(self.cache)

def get_brewery_location(brewery_name):
    webdriver_service = Service('/usr/local/bin/chromedriver')
    webdriver_service.start()
    
    #launch
    driver = webdriver.Chrome(service=webdriver_service)
    driver.get("https://www.google.com")
    
    #find the search box and input the brewery name
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(brewery_name)
    
    #press Enter to perform the search
    search_box.send_keys(Keys.RETURN)
    
    #wait for the search results 
    driver.implicitly_wait(5)
    
    #find the first search result element
    first_result = driver.find_element(By.CSS_SELECTOR, "div#rhs.TQc1id.rhstc4")
    
    #find the address
    address = first_result.find_element(By.CSS_SELECTOR, "span.LrzXr").text
    
    driver.quit()
    
    return address 

def extract_city_country(address):
    #regex for pattern matching
    foreign_city = "^\d+\s[\w\s]+$"
    us_state = "^[A-Z]{2}\s\d+"

    #split the address into parts based on comma
    parts = address.split(', ')
    
    #the last part usually contains state/county info
    # if US, remove state and zipcode and replace with country
    country = parts[-1]
    if(re.match(us_state, country)):
        country = 'USA'
    
    #the second-to-last part usually contains city info
    # if non-US, this will have postal code included (i.e "40211 Düsseldorf"), need to remove postal code
    city = parts[-2]
    if(re.match(foreign_city, city)):
        city = city.split()[-1]

    return city, country

def add_locations(df):
    cache = Cache(1000)
    df["City"] = ""
    df["Country"] = ""

    for index, row in df.iterrows():
        try:
            brewery = row["Brewery"]
            if (cache.get(brewery) == None):
                city, country = extract_city_country(get_brewery_location(row["Brewery"]))
                df.at[index, 'City'] = city
                df.at[index, 'Country'] = country

                cache.set(brewery, {'City': city, 'Country': country})
            else: 
                value = cache.get(brewery)
                df.at[index, 'City'] = value['City']
                df.at[index, 'Country'] = value['Country']
        except IndexError:
            df.drop(index, inplace=True)
        except common.exceptions.NoSuchElementException:
            df.drop(index, inplace=True)
    
    return df

# Test Code
# brewery_name = "Privatbrauerei Frankenheim"
# brewery_address = (get_brewery_location(brewery_name))
# city, country = extract_city_country(brewery_address)
# print("City:", city)
# print("Country:", country)

input_file_path = 'beer.csv'
df = pd.read_csv(input_file_path)

updated = add_locations(df)

output_file_path = 'beer_with_locations.csv'
updated.to_csv(output_file_path, index=False)