import os
import re
import configparser
import shutil


def remplace_texte_dans_fichier(fichier, remplacements):
    try:
        with open(fichier, 'r', encoding='utf-8') as file:
            contenu = file.read()
            nouveau_contenu = contenu

            for i in range(1, 3):
                texte_a_remplacer = remplacements[f"texte{i}_a_remplacer"]
                remplacement = remplacements[f"remplacement{i}"]
                nouveau_contenu = re.sub(texte_a_remplacer, remplacement, nouveau_contenu, flags=re.M)

        with open(fichier, 'w', encoding='utf-8') as file:
            file.write(nouveau_contenu)
    except Exception as e:
        print(f"Erreur lors du traitement de {fichier}: {str(e)}")


def remplace_texte_dans_repertoire(repertoire_source, remplacements, repertoire_destination):
    for dossier, sous_dossiers, fichiers in os.walk(repertoire_source):
        for fichier in fichiers:
            chemin_fichier = os.path.join(dossier, fichier)
            remplace_texte_dans_fichier(chemin_fichier, remplacements)
            # Créez le chemin du fichier dans le répertoire de destination
            chemin_fichier_destination = os.path.join(repertoire_destination,
                                                      os.path.relpath(chemin_fichier, repertoire_source))

            # Assurez-vous que le répertoire de destination existe
            os.makedirs(os.path.dirname(chemin_fichier_destination), exist_ok=True)

            # Copiez le fichier avec son chemin complet dans le répertoire de destination
            shutil.copy2(chemin_fichier, chemin_fichier_destination)
            print(f"Fichier copié et traité : {chemin_fichier_destination}")


if __name__ == "__main__":
    # Lecture du fichier de configuration
    config = configparser.ConfigParser()
    config.read("config.ini")

    repertoire_source = config.get("Configuration", "repertoire_source")
    repertoire_destination = config.get("Configuration", "repertoire_destination")

    remplacements = {}
    for i in range(1, 3):
        texte_a_remplacer = config.get("Configuration", f"texte{i}_a_remplacer")
        remplacement = config.get("Configuration", f"remplacement{i}")
        remplacements[f"texte{i}_a_remplacer"] = texte_a_remplacer
        remplacements[f"remplacement{i}"] = remplacement

    # Remplacement de texte dans le répertoire source
    remplace_texte_dans_repertoire(repertoire_source, remplacements, repertoire_destination)
