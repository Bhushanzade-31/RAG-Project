import pandas as pd
from pathlib import Path

# ---- dataset summary (computed once at startup) ----
_df = pd.read_csv(Path(__file__).parent / "HRDataset_v14_short.csv", encoding="utf-8-sig")
for c in ["Sex", "Department", "Position", "State", "EmploymentStatus", "PerformanceScore"]:
    _df[c] = _df[c].astype(str).str.strip()


def _stats_text():
    lines = [f"Total employees in dataset: {len(_df)}"]
    for col in ["Sex", "Department", "EmploymentStatus", "PerformanceScore", "State"]:
        counts = _df[col].value_counts().to_dict()
        lines.append(f"{col} counts: {counts}")
    lines.append(f"Average salary: {_df['Salary'].mean():.0f}")
    lines.append(f"Average salary by department: {_df.groupby('Department')['Salary'].mean().round(0).to_dict()}")
    lines.append(f"Average salary by Sex: {_df.groupby('Sex')['Salary'].mean().round(0).to_dict()}")
    return "\n".join(lines)


STATS = _stats_text()


def rag_simple(query, retriever, llm, top_k=5):
    results = retriever.retrieve(query, top_k=top_k)
    context = "\n\n".join(doc["content"] for doc in results) if results else ""
    if not context:
        return "No relevant content found in the results"

    prompt = f"""Answer using the dataset summary and the employee records below.
For counts, totals and averages use the summary. For details about specific people use the records.
If neither contains the answer, say so.

Dataset summary:
{STATS}

Employee records:
{context}

Question: {query}

Answer:"""

    response = llm.invoke(prompt)
    content = response.content
    answer = content if isinstance(content, str) else "".join(
        p.get("text", "") if isinstance(p, dict) else str(p) for p in content
    )
    return answer