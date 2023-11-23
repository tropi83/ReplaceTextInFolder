import os
import re
import configparser
import shutil
from datetime import datetime
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog

class TextReplacementApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Text Replacement Tool')
        self.setGeometry(300, 300, 400, 200)

        self.source_label = QLabel('Source Directory:')
        self.source_line_edit = QLineEdit()
        self.source_browse_button = QPushButton('Browse')
        self.destination_label = QLabel('Destination Directory:')
        self.destination_line_edit = QLineEdit()
        self.destination_browse_button = QPushButton('Browse')
        self.replace_button = QPushButton('Replace Text')
        self.status_label = QLabel('Status:')

        self.source_browse_button.clicked.connect(self.browse_source)
        self.destination_browse_button.clicked.connect(self.browse_destination)
        self.replace_button.clicked.connect(self.replace_text)

        layout = QVBoxLayout()
        layout.addWidget(self.source_label)
        layout.addWidget(self.source_line_edit)
        layout.addWidget(self.source_browse_button)
        layout.addWidget(self.destination_label)
        layout.addWidget(self.destination_line_edit)
        layout.addWidget(self.destination_browse_button)
        layout.addWidget(self.replace_button)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def browse_source(self):
        directory = QFileDialog.getExistingDirectory(self, 'Select Source Directory')
        if directory:
            self.source_line_edit.setText(directory)

    def browse_destination(self):
        directory = QFileDialog.getExistingDirectory(self, 'Select Destination Directory')
        if directory:
            self.destination_line_edit.setText(directory)

    def replace_text(self):
        source_path = self.source_line_edit.text()
        destination_path = self.destination_line_edit.text()

        if not source_path or not destination_path:
            self.status_label.setText('Please select both source and destination directories.')
            return

        config_file_path = "config.ini"
        config = configparser.ConfigParser()

        if os.path.exists(config_file_path):
            config.read(config_file_path)
        else:
            self.status_label.setText(f"Configuration file {config_file_path} not found.")
            return

        repertoire_source = config.get("Configuration", "repertoire_source", fallback='')
        repertoire_destination = config.get("Configuration", "repertoire_destination", fallback='')

        if not repertoire_source:
            repertoire_source = source_path
        if not repertoire_destination:
            repertoire_destination = destination_path

        remplacements = {}
        for i in range(1, 3):
            texte_a_remplacer = config.get("Configuration", f"texte{i}_a_remplacer", fallback='')
            remplacement = config.get("Configuration", f"remplacement{i}", fallback='')
            remplacements[f"texte{i}_a_remplacer"] = texte_a_remplacer
            remplacements[f"remplacement{i}"] = remplacement

        # Get the current date for the destination folder name
        current_date = datetime.now()
        repertoire_destination = os.path.join(repertoire_destination, current_date.strftime("%d-%m-%y"))

        # Replacement of text in the source directory
        self.remplace_texte_dans_repertoire(repertoire_source, remplacements, repertoire_destination)
        self.status_label.setText(f"Text replacement completed in {repertoire_source}. Output in {repertoire_destination}.")

    def remplace_texte_dans_fichier(self, fichier, remplacements):
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

    def remplace_texte_dans_repertoire(self, repertoire_source, remplacements, repertoire_destination):
        for dossier, sous_dossiers, fichiers in os.walk(repertoire_source):
            for fichier in fichiers:
                chemin_fichier = os.path.join(dossier, fichier)
                self.remplace_texte_dans_fichier(chemin_fichier, remplacements)

                # Create the path of the file in the destination directory
                chemin_fichier_destination = os.path.join(repertoire_destination,
                                                          os.path.relpath(chemin_fichier, repertoire_source))

                # Ensure that the destination directory exists
                os.makedirs(os.path.dirname(chemin_fichier_destination), exist_ok=True)

                # Copy the file with its full path to the destination directory
                shutil.copy2(chemin_fichier, chemin_fichier_destination)
                print(f"File copied and processed: {chemin_fichier_destination}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TextReplacementApp()
    window.show()
    sys.exit(app.exec_())
