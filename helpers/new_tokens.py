import threading
import asyncio
import websockets
import json
from helpers.database import INITIAL_STATE
from datetime import datetime

async def subscribe():
  uri = "wss://pumpportal.fun/api/data"
  async with websockets.connect(uri) as websocket:
      
      # Subscribing to token creation events
      payload = {
          "method": "subscribeNewToken",
      }
      await websocket.send(json.dumps(payload))
      
      async for message in websocket:
          contract = json.loads(message)
          if contract.get('mint'):
            INITIAL_STATE.insert_one(
              {
                  'mint': contract['mint'],
                  'state': 'initial',
                  'createdAt': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              }
            )

def run_subscribe():
  asyncio.new_event_loop().run_until_complete(subscribe())

# Run the subscribe function
new_token_thread = threading.Thread(target=run_subscribe, daemon=True)
new_token_thread.start()
