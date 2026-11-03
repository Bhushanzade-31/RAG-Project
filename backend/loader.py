from pathlib import Path
from langchain_community.document_loaders.csv_loader import CSVLoader

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "C:\\Users\\zadeg\\OneDrive\\Desktop\\RAG\\backend\\HRDataset_v14_short.csv"   # keep the CSV next to this script

loader = CSVLoader(
    file_path=str(CSV_PATH),
   # metadata_columns=["Employee_Name", "EmpID", "Department", "Position"],
    csv_args={"delimiter": ","},
    encoding="utf-8-sig",
)

data = loader.load()
print(len(data))
print(data[0].metadata)
print(data[0].page_content)   # should now show Salary, State, PerformanceScore, etc.
