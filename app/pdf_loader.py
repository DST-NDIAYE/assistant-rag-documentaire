import fitz

def extraire_texte_pdf(chemin_pdf: str) -> str:
   
    liste_pages = []

    with fitz.open(chemin_pdf) as doc:
        for page in doc:
            texte = page.get_text()

            if texte.strip():
                liste_pages.append(texte)

    return "\n".join(liste_pages)



