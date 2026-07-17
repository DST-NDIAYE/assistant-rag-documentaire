from pathlib import Path

import fitz
from langchain_core.documents import Document


def extraire_pages_pdf(path_documents: str) -> list[Document]:
    dossier = Path(path_documents)

    if not dossier.exists():
        raise FileNotFoundError(
            f"Le dossier n'existe pas : {path_documents}"
        )

    if not dossier.is_dir():
        raise NotADirectoryError(
            f"Le chemin fourni n'est pas un dossier : {path_documents}"
        )

    chemins_pdf = list(dossier.glob("*.pdf"))

    if not chemins_pdf:
        raise FileNotFoundError(
            f"Aucun fichier PDF trouvé dans : {path_documents}"
        )

    documents_complets = []

    for chemin_pdf in chemins_pdf:
        documents_pdf = []

        with fitz.open(chemin_pdf) as pdf:
            for numero_page, page in enumerate(pdf, start=1):
                texte = page.get_text("text").strip()

                if not texte:
                    continue

                document = Document(
                    page_content=texte,
                    metadata={
                        "source": chemin_pdf.name,
                        "page": numero_page
                    }
                )

                documents_pdf.append(document)

        if not documents_pdf:
            print(
                f"Aucun texte extrait de {chemin_pdf.name}. "
                "Un traitement OCR est peut-être nécessaire."
            )
            continue

        documents_complets.extend(documents_pdf)

    if not documents_complets:
        raise ValueError(
            "Aucun texte n'a pu être extrait des fichiers PDF."
        )

    return documents_complets