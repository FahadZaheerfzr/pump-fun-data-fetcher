from database import TOKENS
from datetime import datetime
import requests
import time
import threading

def one_hour_update():
  tokens = TOKENS.find({"state": "fifteen_minutes"})

  for token in tokens:
    token_update_date = token["updatedAt"]

    # Check if token has been updated for 1 hour
    current_time = datetime.now()

    time_difference = current_time - token_update_date

    if time_difference.total_seconds() >= 3600:
        response = requests.get(f"https://api.dexscreener.com/latest/dex/tokens/{token['contractAddress']}")
        data = response.json()

        hourly_info = data["pairs"][0]
        TOKENS.update_one(
          {"contractAddress": token["contractAddress"]},
          {
            "$set": {
              ""
              "mcapEveryH": hourly_info["fdv"],
              "mcapATH/mcap15min": token['allTimeHighMcap'] / hourly_info['fdv'],
              "allTimeHighMcap": hourly_info['fdv'] if hourly_info['fdv'] > token['allTimeHighMcap'] else token['allTimeHighMcap'],
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