from agent import movie_agent
import os
print("Loaded API Key:", os.getenv("OPENAI_API_KEY"))


def main():
    print("🎬 Movie Agent is running! Type 'exit' to quit.\n")

    while True:
        user_input = input("🧑 You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("👋 Exiting Movie Agent. Bye!")
            break

        result = movie_agent(user_input)

        print("\n🤖 Agent Response:")

        # 🚨 Handle clarification cases where clarification is needed
        if result.get("status") == "clarification_needed":
            print(result.get("message"))

            suggestions = result.get("suggestions", [])
            if suggestions:
                print("Did you mean:")
                for s in suggestions:
                    print(f" - {s}")

        # ✅ Handle success case
        elif result.get("status") == "success":
            print(f"🎥 Movie: {result.get('movie')}")
            print(f"📍 In Theaters: {result.get('in_theaters')}")
            print(f"🎟️ BookMyShow Available: {result.get('bookmyshow_available')}")

        # ⚠️ fallback
        else:
            print("Something went wrong:", result)

        print("\n" + "-" * 50 + "\n")


if __name__ == "__main__":
    main()