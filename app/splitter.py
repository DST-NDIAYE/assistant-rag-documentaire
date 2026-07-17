from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def creer_chunks( documents : list[Document], chunk_size=1000, chunk_overlap=100 ) -> list[Document] :
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size , 
        chunk_overlap = chunk_overlap , 
        separators= ["\n\n" , "\n" , " " , ""]
    )
    
    return  splitter.split_documents(documents)

     
    