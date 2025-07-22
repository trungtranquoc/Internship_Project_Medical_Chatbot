from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_experimental.text_splitter import SemanticChunker
# from langchain_text_splitters import MarkdownHeaderTextSplitter
import pandas as pd
import os
from tqdm import tqdm

METADATA_PATH = 'data/metadata_df.csv'

def load_markdown(path):
    """Load a markdown file as a LangChain Document."""
    return TextLoader(path, encoding="utf-8").load()

def chunk_by_semantic(path, embedding, breakpoint_threshold_amount=60, number_of_chunks=600):
    """Split documents into chunks using LangChain's semantic chunker."""
    documents = load_markdown(path)
    documents = [doc.page_content for doc in documents]
    
    text_splitter = SemanticChunker(
        embeddings = embedding.get_embedding(),
        breakpoint_threshold_type='percentile',
        breakpoint_threshold_amount=breakpoint_threshold_amount,
        number_of_chunks=number_of_chunks
    )

    return text_splitter.create_documents(documents)

def chunk_by_recursive(path, chunk_size=500, chunk_overlap=100):
    """Split documents into chunks using LangChain's text splitter."""
    documents = load_markdown(path)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    return splitter.split_documents(documents)

def markdown_recursive_chunking(path, chunk_size=1000, chunk_overlap=200):
    """
    Advanced version using regex patterns for more flexible header detection.

    Args:
        chunk_size: Maximum number of characters per chunk
        chunk_overlap: Number of characters to overlap between chunks
    
    Returns:
        RecursiveCharacterTextSplitter configured for markdown with regex
    """
    documents = load_markdown(path)

    # Regex patterns for different markdown elements
    separators = [
        r"\n#{2,6} ",     # H2-H6 headers (2-6 #'s followed by space)
        r"\n#{1} ",       # H1 headers (single # followed by space)
        r"\n\n",          # Paragraph breaks
        r"\n",            # Line breaks
        r" ",             # Word boundaries
        r""               # Character level
    ]
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators,
        is_separator_regex=True
    )
    
    return splitter.split_documents(documents)

def chunk_multiple_files(directory, chunk_fn, **args):
    """
        - Chunk multiple files using a chunking function with return metadata
        - Auto adding metadata to each chunk: file_name, year and directory
    """
    metadata = pd.read_csv(METADATA_PATH)
    all_chunks = []

    for data in tqdm(metadata.itertuples()):
        path = os.path.join(directory, data[2])
        all_chunks += [(chunk.page_content, data[1], data[2], data[3]) for chunk in chunk_fn(path, **args)]

    return all_chunks   # List: [(chunk, year, file_name, directory)]

