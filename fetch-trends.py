from pytrends.request import TrendReq
import pandas as pd
import time
import os

# List of German region geocodes
de_region_geocodes = [
    'DE-BW', 'DE-BY', 'DE-BE', 'DE-BB', 'DE-HB', 'DE-HH', 'DE-HE', 'DE-MV',
    'DE-NI', 'DE-NW', 'DE-RP', 'DE-SL', 'DE-SN', 'DE-ST', 'DE-SH', 'DE-TH'
]

def fetch_trends_data(keywords, regions, timeframe='2020-06-04 2024-06-04'):
    pytrends = TrendReq(hl='de-DE', tz=0)  # Use German locale and timezone
    all_data = pd.DataFrame()

    for region in regions:
        for keyword in keywords:
            try:
                pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=region, gprop='')
                interest_over_time_df = pytrends.interest_over_time()
                if not interest_over_time_df.empty:
                    interest_over_time_df = interest_over_time_df.drop(columns=['isPartial'])
                    interest_over_time_df['region'] = region
                    interest_over_time_df['keyword'] = keyword
                    all_data = pd.concat([all_data, interest_over_time_df])
                    print(f"Collected data for {keyword} in {region}")
                else:
                    print(f"No data for {keyword} in {region}.")
                time.sleep(60)  # Wait for 60 seconds to avoid hitting the rate limit
            except Exception as e:
                print(f"An error occurred for keyword {keyword} in {region}: {e}")
                time.sleep(60)  # Wait for 60 seconds before retrying with the next keyword

    if not all_data.empty:
        file_path = os.path.join('data', 'combined_trends_data_by_region_de.csv')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        all_data.to_csv(file_path, index=False)
        print(f"Saved combined data to {file_path}")
    else:
        print("No data collected for any keyword.")

if __name__ == "__main__":
    kw_list = [
        "smartphone", "laptop", "headphones", "tablet", "smartwatch",
    ]
    fetch_trends_data(kw_list, de_region_geocodes, timeframe='2020-06-04 2024-06-04')
