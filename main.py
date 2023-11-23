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


def rename_files_and_folders(config):
    # Parcourez les différentes clés de remplacement
    for i in range(1, 4):  # Pour texte1_a_remplacer, texte2_a_remplacer, texte3_a_remplacer
        key_to_replace = config.get('Configuration', f"texte{i}_a_remplacer")

        # Parcourez tous les fichiers et sous-dossiers dans le dossier spécifié
        for root, dirs, files in os.walk(config.get('Configuration', 'repertoire_source'), topdown=False):
            for file_name in files:
                # Construisez le chemin complet du fichier
                file_path = os.path.join(root, file_name)

                # Vérifiez si la clé à remplacer est présente dans le nom du fichier
                if key_to_replace in file_name:
                    # Construisez le nouveau nom de fichier en remplaçant la clé
                    new_file_name = file_name.replace(key_to_replace, config.get('Configuration', f"remplacement{i}"))

                    # Construisez le nouveau chemin du fichier
                    new_file_path = os.path.join(root, new_file_name)

                    # Renommez le fichier
                    os.rename(file_path, new_file_path)
                    print(f"Renommage : {file_path} -> {new_file_path}")

            # Construisez le nouveau nom de dossier en remplaçant la clé
            if key_to_replace in root:
                new_folder_name = root.replace(key_to_replace, config.get('Configuration', f"remplacement{i}"))

                # Construisez le nouveau chemin du dossier
                new_folder_path = os.path.join(os.path.dirname(root), new_folder_name)

                # Renommez le dossier
                os.rename(root, new_folder_path)
                print(f"Renommage du dossier : {root} -> {new_folder_path}")


if __name__ == "__main__":
    # Lecture du fichier de configuration
    config = configparser.ConfigParser()
    config_file_path = "config.ini"

    if os.path.exists(config_file_path):
        config.read(config_file_path)
    else:
        print(f"Le fichier de configuration {config_file_path} n'a pas été trouvé.")
        exit()

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
    #rename_files_and_folders(config)
