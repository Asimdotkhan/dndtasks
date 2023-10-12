import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd

def perform_scraping(endpoints):
    base_url = "https://ecoprofile.infometrics.co.nz/Ashburton%20District/"

    scraped_data = []

    for endpoint in tqdm(endpoints, desc="Scraping Endpoints"):
        url = f"{base_url}{endpoint}"

        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            select_element = soup.find('select', attrs={'name': 'compareAreaId'})

            if select_element:
                areas = select_element.find_all('option')
                for area in tqdm(areas, desc="Scraping Areas", leave=False):
                    
                    area_id = area['value']
                    area_name = area.get_text(strip=True)

                    area_url = f"{url}?compareAreaId={area_id}"
                    area_response = requests.get(area_url)

                    if area_response.status_code == 200:
                        area_soup = BeautifulSoup(area_response.content, 'html.parser')
                        tbody = area_soup.find('tbody')

                        if tbody:
                            rows = tbody.find_all('tr')

                            for row in rows:
                                cells = row.find_all('td')
                                row_data = [area_name] + [cell.get_text(strip=True) for cell in cells]
                                scraped_data.append(row_data)
                        else:
                            print(f"Table body not found for {area_name} in {endpoint}.")
                    else:
                        print(f"Failed to fetch data for {area_name} in {endpoint}.")
            else:
                print(f"Select element not found on the page for {endpoint}.")
        else:
            print(f"Failed to fetch data from the URL: {url} for {endpoint}.")
    

    return scraped_data


def get_industry_data(endpoints):
    base_url = "https://ecoprofile.infometrics.co.nz/Ashburton%20District/"

    scraped_data = []

    for endpoint in tqdm(endpoints, desc="Scraping Endpoints"):
        url = f"{base_url}{endpoint}"

        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract available years from the "year" select element
            year_select_element = soup.find('select', attrs={'name': 'year'})
            if year_select_element:
                years = [option['value'] for option in year_select_element.find_all('option')]

                for year in tqdm(years, desc="Scraping Years", leave=False):
                    select_element = soup.find('select', attrs={'name': 'compareAreaId'})

                    if select_element:
                        areas = select_element.find_all('option')
                        for area in tqdm(areas, desc="Scraping Areas", leave=False):

                            area_id = area['value']
                            area_name = area.get_text(strip=True)

                            area_url = f"{url}?compareAreaId={area_id}&year={year}"
                            area_response = requests.get(area_url)

                            if area_response.status_code == 200:
                                area_soup = BeautifulSoup(area_response.content, 'html.parser')
                                tbody = area_soup.find('tbody')

                                if tbody:
                                    rows = tbody.find_all('tr')

                                    for row in rows:
                                        cells = row.find_all('td')
                                        row_data = [area_name] + [year] + [cell.get_text(strip=True) for cell in cells]
                                        scraped_data.append(row_data)
                                else:
                                    print(f"Table body not found for {area_name} in {endpoint} for year {year}.")
                            else:
                                print(f"Failed to fetch data for {area_name} in {endpoint} for year {year}.")
                    else:
                        print(f"Select element not found on the page for {endpoint} for year {year}.")
            else:
                print(f"No years found for {endpoint}.")
        else:
            print(f"Failed to fetch data from the URL: {url} for {endpoint}.")
    
    return scraped_data

def get_chart_data(endpoint):
    base_url = "https://ecoprofile.infometrics.co.nz/Ashburton%20District/"
    area_data = [
    {"value": "86", "name": "New Zealand"},
    {"value": "84", "name": "Auckland"},
    {"value": "4", "name": "Bay of Plenty Region"},
    {"value": "64", "name": "Buller District"},
    {"value": "58", "name": "Carterton District"},
    {"value": "77", "name": "Central Otago District"},
    {"value": "80", "name": "Clutha District"},
    {"value": "18", "name": "Far North District"},
    {"value": "65", "name": "Grey District"},
    {"value": "25", "name": "Hamilton City"},
    {"value": "22", "name": "Hauraki District"},
    {"value": "51", "name": "Horowhenua District"},
    {"value": "20", "name": "Kaipara District"},
    {"value": "52", "name": "Kapiti Coast District"},
    {"value": "35", "name": "Kawerau District"},
    {"value": "55", "name": "Lower Hutt City"},
    {"value": "48", "name": "Manawatu District"},
    {"value": "62", "name": "Marlborough District"},
    {"value": "16", "name": "Marlborough Region"},
    {"value": "57", "name": "Masterton District"},
    {"value": "61", "name": "Nelson City"},
    {"value": "56105", "name": "New Zealand excl Auckland"},
    {"value": "1", "name": "Northland Region"},
    {"value": "36", "name": "Opotiki District"},
    {"value": "12", "name": "Otago Region"},
    {"value": "27", "name": "Otorohanga District"},
    {"value": "49", "name": "Palmerston North City"},
    {"value": "53", "name": "Porirua City"},
    {"value": "78", "name": "Queenstown-Lakes District"},
    {"value": "47", "name": "Rangitikei District"},
    {"value": "33", "name": "Rotorua District"},
    {"value": "45", "name": "Ruapehu District"},
    {"value": "70", "name": "Selwyn District"},
    {"value": "44", "name": "South Taranaki District"},
    {"value": "28", "name": "South Waikato District"},
    {"value": "43", "name": "Stratford District"},
    {"value": "7", "name": "Taranaki Region"},
    {"value": "60", "name": "Tasman District"},
    {"value": "32", "name": "Tauranga City"},
    {"value": "21", "name": "Thames-Coromandel District"},
    {"value": "72", "name": "Timaru District"},
    {"value": "54", "name": "Upper Hutt City"},
    {"value": "23", "name": "Waikato District"},
    {"value": "3", "name": "Waikato Region"},
    {"value": "26", "name": "Waipa District"},
    {"value": "76", "name": "Waitaki District"},
    {"value": "56", "name": "Wellington City"},
    {"value": "9", "name": "Wellington Region"},
    {"value": "10", "name": "West Coast Region"},
    {"value": "31", "name": "Western Bay of Plenty District"},
    {"value": "66", "name": "Westland District"},
    {"value": "34", "name": "Whakatane District"},
    {"value": "19", "name": "Whangarei District"},
]

    flat_data = []
    header = ["Area", "Year", "Ashburton District", "Other Districts"]

    for area in tqdm(area_data, desc="Fetching Data"):
        full_url = f"{base_url}{endpoint}?compareAreaId={area['value']}"
        response = requests.get(full_url)

        if response.status_code == 200:
            data = response.json()
            data_array = data.get("data", [])

            for row in data_array[1:]:
                year, ashburton_district, other_districts = row[0], row[1], row[2]
                area_name = area['name']

                flat_data.append([area_name, year, ashburton_district, other_districts])
        else:
            print(f"Failed to fetch data for area {area['name']}")

    csv_data = pd.DataFrame(flat_data, columns=header)
    return csv_data


