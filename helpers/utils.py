import requests
import json
import certifi


def get_holder_account_owner(holder_account):
  url = 'https://twilight-chaotic-lake.solana-mainnet.quiknode.pro/62079590bd7ea8e94ed1aa6355931eeab2f459da/'


  headers = {
      "Content-Type": "application/json"
  }
  data = {
      "jsonrpc": "2.0",
      "id": 1,
      "method": "getAccountInfo",
      "params": [holder_account,{"encoding": "jsonParsed"}]
  }


  response = requests.post(url, headers=headers, data=json.dumps(data), verify=certifi.where())

  data = response.json()
  return data['result']['value']['data']['parsed']['info']['owner']


def get_token_holder_count(token_address):
    url = (
        f"https://mainnet.helius-rpc.com/?api-key=f12991da-2b2c-4f83-9f89-d8e7cb47166e"
    )
    params = {"limit": 1000, "mint": token_address}
    headers = {"Content-Type": "application/json"}
    body = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTokenAccounts",
        "params": params,
    }
    response = requests.post(url, headers=headers, data=json.dumps(body),  verify=certifi.where())
    data = response.json()
    total_holders = data['result']["total"]
    return total_holders


def get_solana_top_token_holders(token_address, supply):
    url = "https://twilight-chaotic-lake.solana-mainnet.quiknode.pro/62079590bd7ea8e94ed1aa6355931eeab2f459da/"

    headers = {"Content-Type": "application/json"}
    data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTokenLargestAccounts",
        "params": [token_address],
    }

    response = requests.post(url, headers=headers, data=json.dumps(data),  verify=certifi.where())

    data = response.json()
    

    top_five_holders_percentage = []

    for holder in data["result"]["value"]:
        holder_account = get_holder_account_owner(holder["address"])
        if holder_account == "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1":
            continue
        percentage = (
            holder["uiAmount"] / (float(supply))
        ) * 100
        top_five_holders_percentage.append(percentage)
        if len(top_five_holders_percentage) == 5:
            break

    return ("{:.2f}".format(top_five_holders_percentage[0]), "{:.2f}".format(sum(top_five_holders_percentage)))





def get_ohlc(pair_address, start_time, end_time, interval):
    url = f"https://public-api.birdeye.so/defi/ohlcv?address={pair_address}&type={interval}&time_from={start_time}&time_to={end_time}"
    headers = {
        "accept": "application/json",
        "x-chain": "solana",
        "X-API-KEY": "061eef71caa947a3b82c8dbda8bbdf63",
    }

    response = requests.get(url, headers=headers,  verify=certifi.where())

    if response.status_code != 200:
        raise Exception(f"Error fetching data: {response.status_code}, {response.text}")

    data = response.json()
    print(data)
    open_price = data["data"]["items"][0]["o"]
    high_price = data["data"]["items"][0]["h"]
    return open_price, high_price
