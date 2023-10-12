from flask import Flask, render_template, send_file, request, make_response
from data.file_converter import convert_file
from data.data_downloader import fetch_data
from data.data_scraper import perform_scraping, get_chart_data, get_industry_data
from data.ausdataset import get_latest_available_month, get_data
import pandas as pd
import json
import csv
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def welcome():
    return render_template('index.html')

with open('datasets.json', 'r') as json_file:
    config = json.load(json_file)

@app.route('/fileconverter', methods=['GET', 'POST'])
def file_converter():
    if request.method == 'POST':
        file = request.files['file']
        file_type = request.form.get('file_type')
        convert_to = request.form.get('action')

        converted_file = convert_file(file, file_type, convert_to)

        if converted_file:
            return send_file(converted_file, as_attachment=True)
        else:
            return "Conversion failed."

    return render_template('fileconverter.html')


@app.route('/scraper', methods=['GET', 'POST'])
def scraper():
    endpoints_descriptions = {
        "Gdp/_GrowthTable": "Gross Domestic Product Yearly",
        "Gdp/_54Table":"GDP by 54 Industries",
        "Gdp/_anzsicL1Table":"GDP by ANZSIC Level 1 Industry",
        "Gdp/_HHITable": "HHI Index",
        "Gdp/_cowsTable": "Dairy Cow Numbers",
        "Gdp/_milkTable": "Milk Solids Production (Million kg)",
        "Gdp/_herdTable": "Number of Dairy Herds",
        "Gdp/_hectareTable": "Total Hectares in Dairy Production",
        "Gdp/_payoutTable": "Aggregate Dairy Payout",
        "Employment/_growthData":"Employment growth, 2001-2022",
        "Employment/_GrowthTable": "Filled jobs",
        "Employment/_54Table":"Filled Jobs by 54 Industry Categories",
        "Employment/_anzsicL1Table":"Filled Jobs by ANZSIC Level 1 Industry",
        "Productivity/_productivityGrowthTable": "Productivity",
        "Businesses/_growthTable": "Businesses/_growthTable",
        "Population/_GrowthTable": "Estimated resident population",
        "StandardOfLiving/_earningsTable": "Mean annual earnings($)",
        "Tourism/_tourismGdpTimeseries":"Tourism GDP($m)",
        "Tourism/_tourismGdpTimeseriesData":"Tourism GDP growth, 2001-2022",
        "Tourism/_tourismGdpShareData":"Tourism share of total GDP, 2000-2022",
        "Employment/_unEmploymentTimeSeriesData":"Unemployment Rate Yearly",
        "Employment/_neetTimeSeriesData":"NEET Rate (15-24 Year Olds)",
        "Tourism/_tourismIndustryTable":"Tourism GDP relative to other industries"
    }



    if request.method == 'POST':
        selected_endpoint = request.form.get('endpoints')
        filename = endpoints_descriptions.get(selected_endpoint, 'data') + ".csv"

        if selected_endpoint in ["Employment/_unEmploymentTimeSeriesData", "Employment/_neetTimeSeriesData", "Tourism/_tourismGdpTimeseriesData", "Tourism/_tourismGdpShareData","Employment/_growthData"]:
            csv_data = get_chart_data(selected_endpoint)

        elif selected_endpoint == "Tourism/_tourismIndustryTable":
            scraped_data = get_industry_data([selected_endpoint])
            csv_data = pd.DataFrame(scraped_data, columns=["Area", "Year", "Industry", "Level (Ashburton District)", "Change (Ashburton District)", "", "Level", "Change"])
            
        else:
            scraped_data = perform_scraping([selected_endpoint])
            csv_data = pd.DataFrame(scraped_data, columns=["Area", "Year", "Level (Ashburton District)", "Change (Ashburton District)", "", "Level", "Change"])

        csv_content = csv_data.to_csv(index=False)
        response = make_response(csv_content)
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        response.headers["Content-type"] = "text/csv"
        return response

    return render_template('scraper.html', endpoints=endpoints_descriptions)
    


@app.route('/datadownload', methods=['GET', 'POST'])
def data_download():
    Indicator_descriptions = {
        "GDP_Q": "Gross domestic product",
        "CONS_SPEND_Q": "Consumer spending",
        "EMP_FILLED_Q": "Employment (place of residence)",
        "JOBSEEKER_Q": "Jobseeker Support recipients",
        "UNEMPLOYMENT_Q": "Unemployment Rate",
        "DAIRY_PAYOUT": "Dairy Payout",
        "TOURISM_SPEND_Q": "Tourism Expenditure",
        "GUEST_NIGHTS_Q": "Guest Nights",
        "CONSENTS_RES_Q": "Residential consents",
        "CONSENTS_NONRES_Q": "Non-residential consents",
        "HOUSE_PRICES_Q": "House Values",
        "HOUSE_SALES_Q": "House Sales",
        "VEH_REG_NONCOM_Q": "Car Registrations",
        "VEH_REG_COM_Q": "Commercial vehicle registrations",
    }

    if request.method == 'POST':
        Indicator = request.form.get('indicator')
        Indicator_description = Indicator_descriptions.get(Indicator, 'data')
        data = fetch_data(Indicator)

        if data:
            csv_data = pd.DataFrame(data)
            csv_content = csv_data.to_csv(index=False)

            response = make_response(csv_content)
            response.headers["Content-Disposition"] = f"attachment; filename={Indicator_description}.csv"
            response.headers["Content-type"] = "text/csv"
            return response
        else:
            return "Data fetching failed."

    return render_template('datadownload.html', Indicator_descriptions=Indicator_descriptions)



@app.route('/ausdataset', methods=['GET', 'POST'])
def ausdataset():
    if request.method == 'POST':
        dataset_choice = request.form['dataset']
        chunk_size = int(request.form['chunk_size'])
        
        if dataset_choice not in config:
            return "Invalid dataset choice."
        
        name = config[dataset_choice]["name"]
        Baseurl = config[dataset_choice]["Baseurl"]
        keyending = config[dataset_choice]["keyending"]
        latest_month_url = config[dataset_choice]["latest_month_url"]
        areacode_file_path = config[dataset_choice]["areacode file path"]
        
        latest_month = get_latest_available_month(latest_month_url)

        data_with_labels=get_data(Baseurl,keyending,latest_month,areacode_file_path,chunk_size)

        if data_with_labels:
            with open(name, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(data_with_labels)

            response = make_response(open(name, 'rb').read())
            response.headers["Content-Disposition"] = f"attachment; filename={name}.csv"
            response.headers["Content-type"] = "text/csv"
            os.remove(name)

            return response
        
        else:
            return "Data fetching failed."

    return render_template('ausdataset.html' ,config=config)

if __name__ == '__main__':
    app.run(debug=True)