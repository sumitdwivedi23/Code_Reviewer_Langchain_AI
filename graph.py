from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from llm import ReviewLLM
from prompts import ANALYZE_PROMPT, IMPROVE_PROMPT, REPORT_PROMPT

class ReviewState(TypedDict):
    filename: str
    code: str
    analysis: Optional[str]
    improvements: Optional[str]
    report: Optional[str]
    retry_count: int

class CodeReviewWorkflow:
    def __init__(self):
        self.llm = ReviewLLM()
        self.max_retries = 3

    def analyze_code(self, state: ReviewState) -> ReviewState:
        state["retry_count"] = state.get("retry_count", 0)  # Ensure retry_count exists
        prompt = ANALYZE_PROMPT.format(filename=state["filename"], code=state["code"])
        state["analysis"] = self.llm.generate_text(prompt)
        if not state["analysis"] or len(state["analysis"].split()) < 50:
            state["retry_count"] += 1
            if state["retry_count"] >= self.max_retries:
                print(f"Analysis failed after {self.max_retries} attempts.")
                return state
            print(f"Retrying analysis... (Retry count: {state['retry_count']})")
            return self.analyze_code(state)
        print(f"Analysis: {state['analysis'][:50]}...")
        return state

    def suggest_improvements(self, state: ReviewState) -> ReviewState:
        state["retry_count"] = state.get("retry_count", 0)  # Ensure retry_count exists
        prompt = IMPROVE_PROMPT.format(analysis=state["analysis"], filename=state["filename"], code=state["code"])
        state["improvements"] = self.llm.generate_text(prompt)
        if not state["improvements"] or len(state["improvements"].split()) < 50:
            state["retry_count"] += 1
            if state["retry_count"] >= self.max_retries:
                print(f"Improvement suggestion failed after {self.max_retries} attempts.")
                return state
            print(f"Retrying improvements... (Retry count: {state['retry_count']})")
            return self.suggest_improvements(state)
        print(f"Improvements: {state['improvements'][:50]}...")
        return state

    def generate_report(self, state: ReviewState) -> ReviewState:
        state["retry_count"] = state.get("retry_count", 0)  # Ensure retry_count exists
        prompt = REPORT_PROMPT.format(
            filename=state["filename"],
            code=state["code"],
            analysis=state["analysis"] or "Analysis unavailable.",
            improvements=state["improvements"] or "Improvements unavailable."
        )
        state["report"] = self.llm.generate_text(prompt)
        print(f"Report: {state['report'][:50]}...")
        return state


def build_graph():
    workflow = CodeReviewWorkflow()
    graph = StateGraph(ReviewState)

    graph.add_node("analyze_code", workflow.analyze_code)
    graph.add_node("suggest_improvements", workflow.suggest_improvements)
    graph.add_node("generate_report", workflow.generate_report)

    graph.add_edge("analyze_code", "suggest_improvements")
    graph.add_edge("suggest_improvements", "generate_report")
    graph.add_edge("generate_report", END)

    graph.set_entry_point("analyze_code")
    return graph.compile()


if __name__ == "__main__":
    with open("add.py", "r") as f:
        code = f.read()
    graph = build_graph()
    result = graph.invoke({"filename": "add.py", "code": code, "retry_count": 0})
    print(result.get("report", "No report generated"))
