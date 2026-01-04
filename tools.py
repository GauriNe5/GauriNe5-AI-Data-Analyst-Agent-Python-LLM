from __future__ import annotations
import pandas as pd


def load_csv(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)


def summarize(df: pd.DataFrame) -> str:
    lines = []
    lines.append(f"Rows: {len(df)}, Columns: {len(df.columns)}")
    lines.append("Columns: " + ", ".join([f"{c} ({df[c].dtype})" for c in df.columns]))
    lines.append("\nPreview:")
    lines.append(df.head(5).to_string(index=False))
    return "\n".join(lines)


def groupby_agg(df: pd.DataFrame, group_col: str, value_col: str, agg: str) -> str:
    if group_col not in df.columns:
        return f"Error: group_col='{group_col}' not in columns: {list(df.columns)}"
    if value_col not in df.columns:
        return f"Error: value_col='{value_col}' not in columns: {list(df.columns)}"

    if agg not in {"mean", "sum", "min", "max", "count"}:
        return f"Error: agg='{agg}' not supported. Use one of: mean,sum,min,max,count"

    grouped = df.groupby(group_col)[value_col].agg(agg).reset_index()
    grouped = grouped.sort_values(by=value_col, ascending=False)
    return grouped.to_string(index=False)


def filter_rows(df: pd.DataFrame, column: str, op: str, value: str) -> str:
    if column not in df.columns:
        return f"Error: column='{column}' not in columns: {list(df.columns)}"

    series = df[column]

    # Try numeric comparison when possible
    def to_number(x: str):
        try:
            return float(x)
        except Exception:
            return None

    value_num = to_number(value)

    if op == "==":
        mask = series.astype(str) == value
    elif op == "!=":
        mask = series.astype(str) != value
    elif op in {">", ">=", "<", "<="}:
        if value_num is None:
            return f"Error: value '{value}' is not numeric for operator '{op}'"
        # Coerce series to numeric
        s_num = pd.to_numeric(series, errors="coerce")
        if op == ">":
            mask = s_num > value_num
        elif op == ">=":
            mask = s_num >= value_num
        elif op == "<":
            mask = s_num < value_num
        else:
            mask = s_num <= value_num
    else:
        return "Error: op must be one of ==, !=, >, >=, <, <="

    out = df[mask].head(50)
    return out.to_string(index=False)
