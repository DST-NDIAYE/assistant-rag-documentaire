import re 


def nettoyer_texte(texte):
    
    texte = texte.lower()
    texte = re.sub(r"\s+", " ", texte)
    return texte.strip()