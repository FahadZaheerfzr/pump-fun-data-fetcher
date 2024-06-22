import requests
from helpers.database import INITIAL_STATE, TOKENS
import threading
import time
from datetime import datetime
from helpers.utils import get_ohlc

def get_raydium_transition():
    initial_contracts = INITIAL_STATE.find({"state": "initial"})

    iterations = 0
    for contract in initial_contracts:
        mint = contract["mint"]
        response = requests.get(
            f" https://api.dexscreener.com/latest/dex/tokens/{mint}"
        )
        data = response.json()

        if data["pairs"] != None:
            print(data)
            for pair in data["pairs"]:
                if pair["dexId"] == "raydium":
                    token_info = requests.get(
                        f"https://pumpportal.fun/api/data/token-info?ca={mint}"
                    ).json()
                    token_info = token_info["data"]
                    total_supply = pair["fdv"] / float(pair["priceUsd"])
                    mcap = (total_supply) * (get_ohlc(mint, int((pair['pairCreatedAt'] / 1000) - 60), int((pair['pairCreatedAt'] / 1000) + 60)))
                    TOKENS.insert_one(
                        {
                            "mcap15min/launch": None,
                            "tgSubs15min": None, # left
                            "launchDate": datetime.fromtimestamp(
                                pair["pairCreatedAt"] / 1000
                            ),
                            "allTimeHighMcap": mcap,
                            "mcapEveryH": mcap,
                            "mcapATH/mcap15min": None, 
                            "Name": token_info["name"],
                            "contractAddress": pair["baseToken"]["address"],
                            "launchMcap": mcap,
                            "mcap15min": None,
                            "liquidity15min": None,
                            "liquidity15min/mcap15min": None,
                            "holders": None,
                            "5minVolume15min": None,
                            "image": (
                                pair["info"]["imageUrl"]
                                if pair.get("info")
                                else token_info["image"]
                            ),
                            "twitter": (
                                token_info["twitter"]
                                if token_info.get("twitter")
                                else None
                            ),
                            "telegram": (
                                token_info["telegram"]
                                if token_info.get("telegram")
                                else None
                            ),
                            "website": (
                                token_info["website"]
                                if token_info.get("website")
                                else None
                            ),
                            "twitterFollowers": None, #left
                            "telegramMembers": None, #left
                            "telegramLiveCall": None, #left
                            "telegramLiveUsers": None, #left
                            "lunarCrushGalaxyScore": None, #left
                            "lunarCrushAltRank": None, #left
                            "lunarCrushSocialDominance": None, #left
                            "lunarCrushSocialScore": None, #left
                            "highestPercetageOfHolder": None,
                            "percentOfTop5Holders": None,
                            "pairAddress": pair["pairAddress"],
                            "quoteToken": pair["quoteToken"]["address"],
                            "liquidity": pair["liquidity"]["usd"],
                            "image": (
                                pair["info"]["imageUrl"]
                                if pair.get("info")
                                else token_info["image"]
                            ),
                            "totalSupply": total_supply,
                            "state": "early",
                            "createdAtDatabase": datetime.now(),
                        }
                    )
                    INITIAL_STATE.update_one(
                        {"mint": mint}, {"$set": {"state": "raydium"}}
                    )

        # Sleep for 1 minute after 300 iterations
        if iterations == 250:
            iterations = 0
            time.sleep(60)

        iterations += 1


def run_raydium_transition():
    while True:
        get_raydium_transition()
        time.sleep(15)


token_transition_thread = threading.Thread(target=run_raydium_transition, daemon=True)
token_transition_thread.start()
