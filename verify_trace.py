import asyncio
import json
from app.agent.orchestrator import handle_chat
from app.models.api_models import Message

async def run_sample_trace():
    print("=" * 75)
    print("🤖 RUNNING AUTOMATED TRACE SIMULATION (SENIOR LEADERSHIP)")
    print("=" * 75)

    # The exact multi-turn conversation inputs from the sample trace
    user_inputs = [
        "We need a solution for senior leadership.",
        "The pool consists of CXOs, director-level positions; people with more than 15 years of experience.",
        "Selection — comparing candidates against a leadership benchmark.",
        "Perfect, that's what we need."
    ]

    chat_history = []

    for idx, user_text in enumerate(user_inputs, 1):
        print(f"\n👉 [TURN {idx}] User says: '{user_text}'")
        
        # Append latest user turn to history state
        chat_history.append(Message(role="user", content=user_text))
        
        # Process through your engine
        response = await handle_chat(chat_history)
        
        # Print output metrics
        print(f"🤖 Agent Reply Preview: {response['reply'][:120]}...")
        print(f"📦 Recommendations Count: {len(response['recommendations'])}")
        print(f"🏁 End Of Conversation Flag: {response['end_of_conversation']}")
        print("-" * 50)
        
        # Append assistant turn to persist conversational memory
        chat_history.append(Message(role="assistant", content=response["reply"]))

    print("\n" + "=" * 75)
    print("✅ TEST COMPLETION: Trace ran from end-to-end smoothly.")
    print("=" * 75)

if __name__ == "__main__":
    asyncio.run(run_sample_trace())