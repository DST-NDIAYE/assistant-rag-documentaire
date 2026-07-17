from pathlib import Path

import fitz
from langchain_core.documents import Document


def extraire_pages_pdf(pdf_path: str) -> list[Document]:
    chemin = Path(pdf_path)

    if not chemin.exists():
        raise FileNotFoundError(f"Le fichier n'existe pas : {pdf_path}")

    documents = []

    with fitz.open(pdf_path) as pdf:
        for numero_page, page in enumerate(pdf, start=1):
            texte = page.get_text("text").strip()

            if not texte:
                continue

            document = Document(
                page_content=texte,
                metadata={
                    "source": chemin.name,
                    "page": numero_page
                }
            )

            documents.append(document)

    if not documents:
        raise ValueError(
            "Aucun texte n'a été extrait du PDF. "
            "Le document nécessite peut-être un traitement OCR."
        )

    return documents