from pathlib import Path

from langchain_community.document_loaders.csv_loader import CSVLoader

loader = CSVLoader(
    file_path=str(Path(__file__).with_name("Iris.csv")),
    metadata_columns=["Species"],
    csv_args={"delimiter": ","}
)
data = loader.load()

print(len(data))
print(data[0].metadata)
print(data[0].page_content)