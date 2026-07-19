from app.pdf_loader import extraire_pages_pdf
from app.text_cleaning import nettoyer_texte , nettoyer_documents
from app.splitter import creer_chunks
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from pathlib import Path

class AssistantDocumentaire:

    def __init__(self, api_key: str , chemin_vectorstore: str = "vectorstore"):
        self.key = api_key

        self.chemin_vectorstore = Path(chemin_vectorstore)
        self.pdf_path = None
        self.texte_complet = None
        self.texte_nettoye = None
        self.chunks = []
        self.embedding = None
        self.vectorstore = None

        self.llm = ChatOpenAI(
            api_key=self.key,
            model="gpt-4.1-mini",
            temperature=0   )



    def creer_vectorstore(self):
        self.embedding = OpenAIEmbeddings(api_key=self.key, model="text-embedding-3-large" )
        self.vectorstore = FAISS.from_documents(
            documents = self.chunks,
            embedding=self.embedding
        )
        self.sauvegarder_vectorstore()


    def vectorstore_existe(self) -> bool:
        fichier_faiss = self.chemin_vectorstore / "index.faiss"
        fichier_pickle = self.chemin_vectorstore / "index.pkl"

        return fichier_faiss.exists() and fichier_pickle.exists()




    def charger_vectorstore(self):
        self.vectorstore = FAISS.load_local ( folder_path=self.chemin_vectorstore , embeddings= self.embedding       )
        


    def sauvegarder_vectorstore(self):
        self.vectorstore.save_local(str(self.chemin_vectorstore))
        print(f"Vectorstore sauvegardé dans : "f"{self.chemin_vectorstore}" )


    def rechercher_passages(self, question: str, k: int = 3):
        if self.vectorstore is None:
            raise ValueError(
                "Aucun document n'a été chargé. "
                "Utilisez d'abord charger_document()."
            )

        resultats = self.vectorstore.similarity_search(
            question,
            k=k
        )

        return resultats
    


    def poser_question(self, question: str, k: int = 3) -> str:
        resultats = self.rechercher_passages( question=question, k=k )

        contexte = "\n\n".join( document.page_content for document in resultats )

        prompt = f"""
        Tu es un assistant d'analyse documentaire.

        Réponds uniquement à partir du contexte fourni.
        Si la réponse n'est pas présente dans le contexte, indique clairement
        que l'information n'a pas été trouvée dans le document.

        Contexte :
        {contexte}

        Question :
        {question} 
        """

        reponse = self.llm.invoke(prompt)

        return {"reponse": reponse,
                "sources": resultats }

