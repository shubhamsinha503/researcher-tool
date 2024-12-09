from langchain_community.document_loaders import UnstructuredURLLoader

# Mock URLs for testing
mock_urls = ["https://www.chittorgarh.com/ipo/sagility-india-ipo/1898/"]

# Load data using UnstructuredURLLoader
try:
    loader = UnstructuredURLLoader(urls=mock_urls)
    data = loader.load()
    # Print the data structure for inspection
    for i, item in enumerate(data):
        print(f"Item {i}: Type - {type(item)}, Content - {item}")
except Exception as e:
    print(f"Error: {e}")

