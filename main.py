import helpers.new_tokens
import time
import helpers.get_raydium
import helpers.fifteen_minutes_info
import helpers.one_hour_update
from helpers.database import TOKENS
from google_sheets import write_to_google_sheets


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
          token['twitterFollowers'],
          None,
          token['telegramLiveCall'],
          token['telegramMembers'],
          str(token['launchDate']),
          token['updatedAt'],
          token['lunarCrushGalaxyScore'],
          token['lunarCrushAltRank'],
          token['lunarCrushSocialDominance'],
          token['lunarCrushSocialScore'],
          token['highestPercetageOfHolder'],
          token['allTimeHighMcap'],
          token['mcapATH/mcap15min'],
          token['Name'],
          f"https://dexscreener.com/solana/{token['contractAddress']}",
          token['launchMcap'],
          token['mcap15min'],
          token['liquidity15min'],
          token['liquidity15min/mcap15min'],
          token['holders'],
          token['5minVolume15min'],
          "1" if token['image'] else "0",
          "1" if token['twitter'] else "0",
          "1" if token['telegram'] else "0",
          "1" if token['website'] else "0",
          token['percentOfTop5Holders'].replace(" ", "") if token['percentOfTop5Holders'] else None,
        ]
      )
    write_to_google_sheets(DATA_TO_INSERT)
    print("Script is running!")
    time.sleep(15)

if __name__ == "__main__":
  main()