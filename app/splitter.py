from langchain_text_splitters import RecursiveCharacterTextSplitter

def creer_chunks( texte, chunk_size=1000, chunk_overlap=100 ) :
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size , 
        chunk_overlap = chunk_overlap , 
        separators= ["\n\n" , "\n" , " " , ""]
    )

    chunks = splitter.split_text(texte)

    return chunks