from app.pdf_loader import extraire_texte_pdf
from app.text_cleaning import nettoyer_texte
from app.splitter import creer_chunks
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS






class AssistantDocumentaire:

    def __init__(self, api_key: str):
        self.key = api_key

        self.pdf_path = None
        self.texte_complet = None
        self.texte_nettoye = None
        self.chunks = []
        self.embedding = None
        self.vectorstore = None


    def creer_vectorstore(self):
        self.embedding = OpenAIEmbeddings(
            api_key=self.key,
            model="text-embedding-3-large"
        )

        self.vectorstore = FAISS.from_texts(
            texts=self.chunks,
            embedding=self.embedding
        )

        return self.vectorstore


    def charger_document(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.texte_complet = extraire_texte_pdf(pdf_path)
        self.texte_nettoye = nettoyer_texte(self.texte_complet)
        self.chunks = creer_chunks(self.texte_nettoye)
        self.creer_vectorstore()






