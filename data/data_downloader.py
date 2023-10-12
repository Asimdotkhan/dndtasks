import requests
from tqdm import tqdm

def fetch_data(Indicator):
    base_api_url = "https://production.infometrics.co.nz/api/qem/data/"
    area_ids = [
        "new-zealand", "northland-region", "bay-of-plenty-region", "marlborough-region", "west-coast-region",
        "far-north-district", "whangarei-district", "kaipara-district", "auckland", "thames-coromandel-district",
        "hauraki-district", "hamilton-city", "waipa-district", "rotorua-district", "whakatane-district",
        "palmerston-north-city", "tararua-district", "horowhenua-district", "kapiti-coast-district", "porirua-city",
        "upper-hutt-city", "lower-hutt-city", "wellington-city", "masterton-district", "marlborough-district",
        "buller-district", "grey-district", "westland-district", "waimakariri-district", "selwyn-district",
        "ashburton-district", "timaru-district", "mackenzie-district", "waitaki-district", "queenstown-lakes-district",
        "clutha-district", "tairawhiti", "manawatu-all", "wairarapa-all", "nelson-tasman",
    ]

    data_list = []
    with tqdm(total=len(area_ids)) as pbar:
        for area_id in area_ids:
            api_url = f"{base_api_url}?area_id={area_id}&series={Indicator}"
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                data = data['series'][0]['values']
                data_list.extend(data)
            pbar.update(1)

    return data_list
