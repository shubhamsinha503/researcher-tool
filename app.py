import requests
from bs4 import BeautifulSoup
import streamlit as st
import google.generativeai as genai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Configure Google API
genai.configure(api_key="AIzaSyBvn8elJo4YhmHkLxy5kGZz4R979z2_Ubg")  # Replace with your actual API key

# UI Enhancements
st.set_page_config(page_title="Gen AI: News Researcher Tool", page_icon="📊", layout="wide")

# Add header and description
st.markdown("<h1 style='text-align: center; color: #FF6347;'>Gen AI: News Researcher Tool</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>A tool that scrapes news, processes data, and answers questions based on aggregated content.</p>", unsafe_allow_html=True)

# Sidebar customization
st.sidebar.header("Enter Your URLs to Research")
url1 = st.sidebar.text_input("Enter URL 1")
url2 = st.sidebar.text_input("Enter URL 2")
url3 = st.sidebar.text_input("Enter URL 3")
process = st.sidebar.button("Process Data", use_container_width=True)

# Main content area
st.write("### Enter your query below to get AI-powered insights:")
question = st.text_input("Your Question:")

all_content = []

# Process URLs
if process:
    if not (url1 or url2 or url3):
        st.error("Please enter at least one valid URL.")
    else:
        st.spinner("Fetching data...")
        urls = [url for url in {url1, url2, url3} if url]
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

                    all_content.append({"title": title, "content": content})
                else:
                    st.error(f"Failed to fetch content from {url}. Status code: {response.status_code}")
            except Exception as e:
                st.error(f"Error fetching {url}: {e}")

        if all_content:
            st.success("Data loaded successfully. Proceeding with text processing...")

            # Step 1: Chunk Splitting
            st.write("Splitting content into chunks...")
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=100,
                separators=["\n", ".", ",", " "]
            )
            docs = []
            for data in all_content:
                chunks = text_splitter.create_documents([data["content"]])
                docs.extend(chunks)

            st.write(f"Split content into {len(docs)} chunks.")

            # Step 2: Generate Embeddings
            st.write("Generating embeddings...")
            try:
                embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
                vector_store = FAISS.from_documents(docs, embeddings)

                # Step 3: Save the Vector Store
                vector_store.save_local("faiss_index")
                st.success("Vector store saved locally.")

                # Step 4: Load Vector Store for Retrieval
                st.write("Loading vector store for retrieval...")
                try:
                    vector_store_loaded = FAISS.load_local(
                        "faiss_index",
                        embeddings,
                        allow_dangerous_deserialization=True  # Ensuring deserialization is explicitly allowed
                    )
                    st.success("Vector store loaded successfully.")
                except Exception as e:
                    st.error(f"Error during vector store loading: {e}")
            except Exception as e:
                st.error(f"Error during embeddings or vector store process: {e}")

# Query handling with the AI model
if question and all_content:
    combined_content = " ".join([data["content"] for data in all_content])

    # Generate the answer using Gemini model
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Answer the following question: {question} based on this content: {combined_content}")

    # Display the response from the model
    st.write("### Answer from Google Gemini model:")
    st.write(response.text)

# Add footer with styling
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Powered by Streamlit, Google Gemini, and LangChain</p>", unsafe_allow_html=True)
