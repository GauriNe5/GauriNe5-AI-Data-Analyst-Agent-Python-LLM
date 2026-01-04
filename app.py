from __future__ import annotations

import json
import os
from dotenv import load_dotenv
from openai import OpenAI

import tools


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


TOOL_DEFS = [
    {
        "type": "function",
        "function": {
            "name": "summarize",
            "description": "Summarize the dataset: row/column count, column names and dtypes, and a preview.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "groupby_agg",
            "description": "Group by a column and aggregate a numeric column.",
            "parameters": {
                "type": "object",
                "properties": {
                    "group_col": {"type": "string", "description": "Column to group by (e.g., department)"},
                    "value_col": {"type": "string", "description": "Numeric column to aggregate (e.g., salary)"},
                    "agg": {"type": "string", "description": "Aggregation: mean, sum, min, max, count"},
                },
                "required": ["group_col", "value_col", "agg"],
                "additionalProperties": False
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "filter_rows",
            "description": "Filter rows by a simple condition.",
            "parameters": {
                "type": "object",
                "properties": {
                    "column": {"type": "string", "description": "Column name to filter on"},
                    "op": {"type": "string", "description": "Operator: ==, !=, >, >=, <, <="},
                    "value": {"type": "string", "description": "Value to compare against (string or number)"},
                },
                "required": ["column", "op", "value"],
                "additionalProperties": False
            },
        },
    },
]


def run_tool(df, tool_name: str, tool_args: dict) -> str:
    if tool_name == "summarize":
        return tools.summarize(df)
    if tool_name == "groupby_agg":
        return tools.groupby_agg(df, **tool_args)
    if tool_name == "filter_rows":
        return tools.filter_rows(df, **tool_args)
    return f"Error: Unknown tool '{tool_name}'"


SYSTEM_PROMPT = """
You are a data analyst agent. Your job is to answer questions about a CSV dataset.
You have access to these tools:
- summarize(): dataset overview
- groupby_agg(group_col, value_col, agg): grouped aggregation
- filter_rows(column, op, value): filtering

Rules:
- If you need to understand the data schema, call summarize first.
- Prefer using tools over guessing.
- After using tools, explain findings clearly for a non-technical stakeholder.
- If a question is ambiguous, choose the most reasonable interpretation and proceed.
"""


def ask_agent(df, user_question: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_question},
    ]

    # Agent loop: allow up to a few tool calls
    for _ in range(5):
        resp = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            tools=TOOL_DEFS,
            tool_choice="auto",
        )

        msg = resp.choices[0].message

        # If the model wants to call tools:
        if msg.tool_calls:
            messages.append({"role": "assistant", "content": msg.content or "", "tool_calls": msg.tool_calls})

            for tc in msg.tool_calls:
                tool_name = tc.function.name
                tool_args = json.loads(tc.function.arguments or "{}")
                tool_result = run_tool(df, tool_name, tool_args)

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": tool_result,
                    }
                )
            continue

        # Otherwise, final answer:
        return msg.content or ""

    return "I reached the maximum number of tool steps. Please rephrase your question more specifically."


def main():
    print("CSV Data Analyst AI Agent (local)")
    file_path = input("Enter CSV path (default: data/sample.csv): ").strip() or "data/sample.csv"

    try:
        df = tools.load_csv(file_path)
    except Exception as e:
        print(f"Failed to load CSV: {e}")
        return

    print("\nLoaded CSV successfully.")
    print("Ask questions like:")
    print("- Summarize this dataset")
    print("- What is the average salary by department?")
    print("- Show employees with salary > 120000\n")

    while True:
        q = input("You: ").strip()
        if q.lower() in {"exit", "quit"}:
            print("Bye.")
            break

        answer = ask_agent(df, q)
        print("\nAgent:\n" + answer + "\n")


if __name__ == "__main__":
    main()
