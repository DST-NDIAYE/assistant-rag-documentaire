import re

from langchain_core.documents import Document


def nettoyer_texte(texte: str) -> str:
    texte = texte.lower()
    texte = re.sub(r"\s+", " ", texte)

    return texte.strip()


def nettoyer_documents(
    documents: list[Document]
) -> list[Document]:
    documents_nettoyes = []

    for document in documents:
        texte_nettoye = nettoyer_texte(
            document.page_content
        )

        if not texte_nettoye:
            continue

        document_nettoye = Document(
            page_content=texte_nettoye,
            metadata=document.metadata.copy()
        )

        documents_nettoyes.append(document_nettoye)

    return documents_nettoyes