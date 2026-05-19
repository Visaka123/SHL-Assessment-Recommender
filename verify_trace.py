import time
import requests

def run_live_render_trace():
    print("=" * 75)
    print("RUNNING LIVE CLOUD TRACE SIMULATION (SENIOR LEADERSHIP)")
    print("=" * 75)

    # Your live Render URL
    url = "https://shl-assessment-recommender-a4ps.onrender.com/chat"

    # The exact multi-turn conversation inputs from the sample trace
    user_inputs = [
        "We need a solution for senior leadership.",
        "The pool consists of CXOs, director-level positions; people with more than 15 years of experience.",
        "Selection — comparing candidates against a leadership benchmark.",
        "Perfect, that's what we need."
    ]

    chat_history = []

    for idx, user_text in enumerate(user_inputs, 1):
        print(f"\n[TURN {idx}] User says: '{user_text}'")
        
        # 1. Append latest user turn to history state
        chat_history.append({"role": "user", "content": user_text})
        
        # 2. Package payload for the POST request
        payload = {"messages": chat_history}
        
        # 3. Fire the live HTTP request to your Render server
        try:
            start_time = time.time()
            response = requests.post(url, json=payload, timeout=30)
            latency = time.time() - start_time
            
            if response.status_code != 200:
                print(f" Error: Received HTTP {response.status_code} from server.")
                print(f"Response content: {response.text}")
                break
                
            data = response.json()
            
            # 4. Print output metrics returned from the cloud
            reply_preview = data.get("reply", "")
            clean_preview = reply_preview.split("\n|")[0][:120].strip()
            
            print(f"Server Latency: {latency:.2f} seconds")
            print(f" Agent Reply Preview: {clean_preview}...")
            print(f" Recommendations Count: {len(data.get('recommendations', []))}")
            print(f" End Of Conversation Flag: {data.get('end_of_conversation', False)}")
            print("-" * 50)
            
            # 5. Append assistant turn to persist conversational memory
            chat_history.append({"role": "assistant", "content": data.get("reply", "")})
            
        except requests.exceptions.Timeout:
            print(" Error: The request timed out (took longer than 30 seconds).")
            break
        except Exception as e:
            print(f" Network Error occurred: {e}")
            break

    print("\n" + "=" * 75)
    print(" TEST COMPLETION: Live cloud trace completed.")
    print("=" * 75)

if __name__ == "__main__":
    run_live_render_trace()