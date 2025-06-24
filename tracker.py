# %%
import os
import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime

# %%
#Setting
COIN = 'bitcoin'
CURRENCY = 'inr'
API_URL = f"https://api.coingecko.com/api/v3/simple/price?ids={COIN}&vs_currencies={CURRENCY}"

# %%
#Fetching the Data

def fetch_data():
    response = requests.get(API_URL) 
    data = response.json()

    if COIN not in data:
        raise Exception("❌ Couldn't fetch coin price.")
    
    price = data[COIN][CURRENCY]
    return {
        "coin" : COIN,
        "price" : price,
        "timestamp" : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    }

# %%
#Saving to CSV

def append_to_csv(record, filename = "price-history.csv"):
    df = pd.DataFrame([record])
    if not os.path.exists(filename):
        df.to_csv(filename, index = False)
    else:
        df.to_csv(filename, mode='a', header=False, index = False)
    print("✅ File Saved to Location")


# %%
#Plotting

def plot_price(filename = "price-history.csv"):
    df = pd.read_csv(filename)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    last_10 = df.tail(10)

    plt.figure(figsize=(10,8))
    plt.plot(last_10['timestamp'], last_10['price'], color = 'green', marker ='o')
    plt.title(f"{COIN.capitalize()} Price Trend (in {CURRENCY.upper()})")
    plt.xlabel("Time")
    plt.ylabel(f"Price ({CURRENCY.upper()})")

    os.makedirs('output', exist_ok=True)
    plt.savefig("output/price_trend.png")

# %%
if __name__ == "__main__":
    try:
        record = fetch_data()
        print(f"🪙 {record['coin'].capitalize()} - ₹ {record['price']}")
        append_to_csv(record)
        plot_price()
    except Exception as e:
        print(str(e))



