from helpers.database import TOKENS
from datetime import datetime
import requests
import time
import threading
from helpers.utils import get_ohlc
import certifi



def one_hour_update():
  tokens = TOKENS.find({"state": "fifteen_minutes"})

  for token in tokens:
    token_update_date = token["updatedAt"]
    token_update_date = datetime.strptime(token_update_date, "%Y-%m-%d %H:%M:%S")
    # Check if token has been updated for 1 hour
    current_time = datetime.now()

    time_difference = current_time - token_update_date
    print(time_difference.total_seconds())
    if time_difference.total_seconds() >= 3600:
        response = requests.get(f"https://api.dexscreener.com/latest/dex/tokens/{token['contractAddress']}", verify=certifi.where())
        data = response.json()
        
        last_updated = datetime.strptime(token['updatedAt'], "%Y-%m-%d %H:%M:%S")
        last_updated_timestamp = int(last_updated.timestamp())
        open_price, high_price = get_ohlc(token['contractAddress'], last_updated_timestamp, last_updated_timestamp+3000, "1H")

        hourly_info = data["pairs"][0]
        high_mcap = token['totalSupply'] * high_price
        TOKENS.update_one(
          {"contractAddress": token["contractAddress"]},
          {
            "$set": {
              "mcapEveryH": hourly_info["fdv"],
              "mcapATH/mcap15min": token['allTimeHighMcap'] / hourly_info['fdv'],
              "allTimeHighMcap": high_mcap if high_mcap > token['allTimeHighMcap'] else token['allTimeHighMcap'],
              "state": "updated",
              "updatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
          },
        )

def run_one_hour_update():
    while True:
        one_hour_update()
        time.sleep(10)

one_hour_update_thread = threading.Thread(target=run_one_hour_update, daemon=True)
one_hour_update_thread.start()