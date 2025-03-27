import sqlite3
from datetime import datetime
from graph import build_graph
from config import LANGSMITH_API_KEY, GROQ_API_KEY

def save_review_to_db(filename: str, code: str, report: str):
    conn = sqlite3.connect("reviews.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            code TEXT,
            report TEXT,
            timestamp TEXT
        )
    """)
    cursor.execute("INSERT INTO reviews (filename, code, report, timestamp) VALUES (?, ?, ?, ?)",
                   (filename, code, report, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def run_code_review(filename: str):
    if not LANGSMITH_API_KEY:
        print("Warning: LangSmith API key missing. Debugging limited.")
    if not GROQ_API_KEY:
        print("Error: GROQ_API_KEY missing. Exiting.")
        return

    try:
        with open(filename, "r") as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return
    except Exception as e:
        print(f"Error reading file '{filename}': {str(e)}")
        return

    graph = build_graph()
    initial_state = {"filename": filename, "code": code}

    print(f"Starting peer review for {filename}:\n{code}")
    try:
        result = graph.invoke(initial_state)
        report = result.get("report")
        if not report:
            print("Error: No review report generated.")
            print(f"Debug state: {result}")
            return

        print("\n=== Peer Review Report ===")
        print(report)

        output_filename = f"review_{filename.replace('.py', '')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(output_filename, "w") as f:
            f.write(report)
        save_review_to_db(filename, code, report)
        print(f"Review saved to {output_filename} and database.")
    except Exception as e:
        print(f"Review process failed: {str(e)}")
        print("Check LangSmith traces for details.")

if __name__ == "__main__":
    filename = input("Enter the Python file to review (e.g., add.py): ")
    run_code_review(filename)