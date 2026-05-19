import os
import requests

OUTPUT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "shl_catalog.json"
)

SHL_LIVE_CATALOG_URL = "https://tcp-us-prod-rnd.shl.com/voiceRater/shl-ai-hiring/shl_product_catalog.json"

def stream_and_save_live_catalog():
    print("=" * 70)
    print(" RAW PACKET STREAMING: BULK SAVING SHL PRODUCTION CATALOG")
    print("=" * 70)
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    
    try:
        print(f" Opening live data stream path:\n{SHL_LIVE_CATALOG_URL}\n")
        
        # 1. Open the request as a raw stream chunk receiver
        response = requests.get(SHL_LIVE_CATALOG_URL, headers=headers, stream=True, timeout=30)
        
        if response.status_code != 200:
            print(f" Connection Intercept: Server responded with status code {response.status_code}")
            return
            
        # 2. Ensure target local storage directories are built
        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        
        # 3. Stream write bytes directly down to disk storage
        with open(OUTPUT_PATH, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk: # Filter out keep-alive header packets
                    file.write(chunk)
                    
        print(" SUCCESS: Raw data stream package fully captured and stored!")
        print(f" File updated: {OUTPUT_PATH}")
        print(f" Size on Disk: {os.path.getsize(OUTPUT_PATH) / 1024:.2f} KB")
        print("=" * 70)

    except Exception as e:
        print(f" Streaming Operation Terminated: {e}")

if __name__ == "__main__":
    stream_and_save_live_catalog()