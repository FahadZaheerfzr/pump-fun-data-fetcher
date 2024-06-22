import helpers.new_tokens
import time
import helpers.get_raydium
import helpers.fifteen_minutes_info
from helpers.database import TOKENS
from google_sheets import write_to_google_sheets
import json

def main():
  while True:
    DATA_TO_INSERT = []
    tokens = TOKENS.find()

    for token in tokens:
      DATA_TO_INSERT.append(
        [
          None,
          token['mcapEveryH'],
          None,
          None,
          token['mcap15min/launch'],
          token['tgSubs15min'],
          str(token['launchDate']),
          token['allTimeHighMcap'],
          token['mcapATH/mcap15min'],
          token['Name'],
          token['contractAddress'],
          token['launchMcap'],
          token['mcap15min'],
          token['mcap15min/launch'],
          token['liquidity15min'],
          token['liquidity15min/mcap15min'],
          token['holders'],
          token['5minVolume15min'],
          token['image'],
          token['twitter'],
          token['telegram'],
          token['website'],
          token['twitterFollowers'],
          token['telegramMembers'],
          token['telegramLiveCall'],
          token['telegramLiveUsers'],
          token['lunarCrushGalaxyScore'],
          token['lunarCrushAltRank'],
          token['lunarCrushSocialDominance'],
          token['lunarCrushSocialScore'],
          token['highestPercetageOfHolder'],
          token['percentOfTop5Holders'],
        ]
      )
    write_to_google_sheets(DATA_TO_INSERT)
    print("Script is running!")
    time.sleep(15)

if __name__ == "__main__":
  main()