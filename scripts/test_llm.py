
import sys

sys.path.append(".")

from crewai import LLM

def test_llm():
    # Test CrewAI LLM directly (same model as embedchain config)
    try:
        llm = LLM(model="gpt-4o-mini", temperature=0)
        response = llm.call("What is data analysis?")
        print("CREWAI LLM RESPONSE:")
        print(response)
    except Exception as e:
        print(f"CREWAI LLM FAILED: {e}")


if __name__ == "__main__":
    test_llm()
