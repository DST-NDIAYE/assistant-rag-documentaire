import fitz


def extraire_texte_pdf(chemin_pdf):
    doc = fitz.open(chemin_pdf)
    print(f"le document contient {len(doc)} pages ")

    liste_page = [ ]
    for page in doc:
        texte = page.get_text()
        if texte.strip() != "" :
            liste_page.append(texte)
        texte_complet = "\n".join(liste_page)
    return texte_complet

