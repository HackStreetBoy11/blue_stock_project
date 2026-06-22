import os
import time
import requests
import pandas as pd

BASE_URL = "https://api.mfapi.in/mf"

SCHEMES = {
    "hdfc_top_100": 125497,
    "sbi_bluechip": 119551,
    "icici_bluechip": 120503,
    "nippon_large_cap": 118632,
    "axis_bluechip": 119092,
    "kotak_bluechip": 120841
}

def fetch_and_save_nav(scheme_name, scheme_code, output_dir="data/raw", max_retries=3):
    os.makedirs(output_dir, exist_ok=True)
    url = f"{BASE_URL}/{scheme_code}"
    
    # Increased initial timeout window to 20 seconds
    timeout = 20 
    
    for attempt in range(1, max_retries + 1):
        print(f"Fetching data for {scheme_name.upper()} (Code: {scheme_code}) - Attempt {attempt}/{max_retries}...")
        try:
            # Increased timeout down below
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            data = response.json()
            
            meta = data.get('meta', {})
            nav_list = data.get('data', [])
            
            if not nav_list:
                print(f"⚠️ No entry found for scheme: {scheme_code}")
                return
                
            df = pd.DataFrame(nav_list)
            df['scheme_code'] = meta.get('scheme_code')
            df['scheme_name'] = meta.get('scheme_name')
            df['fund_house'] = meta.get('fund_house')
            
            cols = ['scheme_code', 'scheme_name', 'fund_house', 'date', 'nav']
            df = df[[c for c in cols if c in df.columns]]
            
            output_file = os.path.join(output_dir, f"{scheme_name}_live.csv")
            df.to_csv(output_file, index=False)
            print(f"✅ Saved to {output_file} | Total Records: {len(df)}\n")
            return  # Success! Break out of the retry loop.
            
        except (requests.exceptions.RequestException, Exception) as e:
            print(f"⚠️ Attempt {attempt} failed due to: {e}")
            if attempt < max_retries:
                sleep_time = attempt * 5  # Waits 5s, then 10s... giving the server room to breathe
                print(f"Sleeping for {sleep_time} seconds before retrying...")
                time.sleep(sleep_time)
            else:
                print(f"❌ Permanent failure for {scheme_name} after {max_retries} attempts.\n")

if __name__ == "__main__":
    print("=== Starting Resilient Live API Data Fetch ===\n")
    for name, code in SCHEMES.items():
        fetch_and_save_nav(name, code)
        # Adding a small polite delay between different funds to avoid hitting rate limits
        time.sleep(2) 
    print("=== Pipeline process completed! ===")