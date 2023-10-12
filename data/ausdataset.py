from datetime import datetime, timedelta
from tqdm import tqdm
import pandas as pd
import requests
import io
import csv


def fetch_data_from_api(url):
    headers = {'Accept': 'application/vnd.sdmx.data+csv;file=true;labels=both'}
    response = requests.get(url, headers=headers)
    return response

def get_latest_available_month(latest_month_url):
    current_date = datetime.now()
    while True:
        latest_month = current_date.strftime("%Y-%m")
        url = latest_month_url.format(latest_month=latest_month)
        response = fetch_data_from_api(url)
        if response.status_code == 200:
            return latest_month
        current_date -= timedelta(days=1)


def get_data(Baseurl,keyending,latest_month,areacode_file_path,chunk_size):   
    Filter = []
    with open(areacode_file_path, "r") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        Filter = [row[0].strip() for row in reader]

    data_with_labels = []
    progress_bar = tqdm(total=len(Filter), desc="Fetching Data")

    for i in range(0, len(Filter), chunk_size):
        filters_chunk = Filter[i:i + chunk_size]
        combined_filter = "+".join(filters_chunk)
        url = f"{Baseurl}{keyending}{combined_filter}.M?startPeriod={latest_month}&endPeriod={latest_month}&dimensionAtObservation=AllDimensions"

        response = fetch_data_from_api(url)

        if response.status_code == 200:
            csv_data = response.text.strip()
            df = pd.read_csv(io.StringIO(csv_data), dtype=str)
            if i == 0:
                data_with_labels.append(list(df.columns)) 
            data_with_labels.extend(df.values.tolist())

        else:
            return f"Failed to get data from URL {url}. Status code: {response.status_code}"

        progress_bar.update(chunk_size)
    progress_bar.close()

    return data_with_labels