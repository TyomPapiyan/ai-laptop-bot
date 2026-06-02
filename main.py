from agent import WebIntelligenceAgent
import json

if __name__ == "__main__":

    agent = WebIntelligenceAgent()

    query = input("💬 Enter query: ")

    result = agent.run(query)

    print("\n🏆 RESULT:\n")

    print(json.dumps(result, indent=2, ensure_ascii=False))