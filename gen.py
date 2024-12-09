import requests
from bs4 import BeautifulSoup
import streamlit as st

st.sidebar.header("Enter your URLs")
url1 = st.sidebar.text_input("URL1")
url2 = st.sidebar.text_input("URL2")
url3 = st.sidebar.text_input("URL3")
process = st.sidebar.button("Process")
st.header("Gen AI: News Researcher Tool")

if process:
    urls = [url for url in {url1, url2, url3} if url]
    if not urls:
        st.error("Please enter at least one valid URL.")
    else:
        all_content = []
        for url in urls:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    st.success(f"Successfully fetched content from {url}")
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Extract meaningful content
                    title = soup.title.string if soup.title else "No Title Found"
                    paragraphs = [p.get_text() for p in soup.find_all('p')]
                    content = "\n".join(paragraphs)

                    st.write(f"Title: {title}")
                    st.write(f"Content: {content[:500]}...")  # Show first 500 characters
                    all_content.append({"title": title, "content": content})
                else:
                    st.error(f"Failed to fetch content from {url}. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"Error fetching {url}: {e}")

        if all_content:
            st.success("Data loaded successfully. Proceeding with text processing...")
            # Further processing like splitting into chunks, embeddings, etc.
