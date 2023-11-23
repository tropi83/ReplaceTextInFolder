import os
import re
import configparser
import shutil
from datetime import datetime
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QProgressBar, QPushButton, QFileDialog, QMessageBox

class TextReplacementApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Text Replacement Tool')
        self.setGeometry(300, 300, 400, 200)

        self.status_label = QLabel('Status:')
        self.progress_bar = QProgressBar()
        self.replace_button = QPushButton('Replace Text')

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.replace_button)
        self.setLayout(layout)

        self.progress_value = 0

        self.replace_button.clicked.connect(self.replace_text)

    def update_progress(self):
        self.progress_bar.setValue(self.progress_value)

    def show_completion_message(self):
        QMessageBox.information(self, 'Text Replacement', 'Text replacement completed.')

    def replace_text(self):
        # Prompt user to select the source directory
        source_dir = QFileDialog.getExistingDirectory(self, 'Select Source Directory')
        if not source_dir:
            self.status_label.setText('Please select a source directory.')
            return

        # Prompt user to select the destination directory
        destination_dir = QFileDialog.getExistingDirectory(self, 'Select Destination Directory')
        if not destination_dir:
            self.status_label.setText('Please select a destination directory.')
            return

        self.progress_value = 0
        self.progress_bar.setValue(0)

        config_file_path = "config.ini"
        config = configparser.ConfigParser()

        if os.path.exists(config_file_path):
            config.read(config_file_path)
        else:
            self.status_label.setText(f"Configuration file {config_file_path} not found.")
            return

        remplacements = {}
        for i in range(1, 3):
            texte_a_remplacer = config.get("Configuration", f"texte{i}_a_remplacer", fallback='')
            remplacement = config.get("Configuration", f"remplacement{i}", fallback='')
            remplacements[f"texte{i}_a_remplacer"] = texte_a_remplacer
            remplacements[f"remplacement{i}"] = remplacement

        # Get the current date for the destination folder name
        current_date = datetime.now()
        repertoire_destination = os.path.join(destination_dir, current_date.strftime("%d-%m-%y"))

        # Calculate the total number of files for progress
        total_files = sum([len(files) for _, _, files in os.walk(source_dir)])

        # Replacement of text in the source directory
        file_count = 0
        for dossier, sous_dossiers, fichiers in os.walk(source_dir):
            for fichier in fichiers:
                chemin_fichier = os.path.join(dossier, fichier)
                self.remplace_texte_dans_fichier(chemin_fichier, remplacements)

                # Create the path of the file in the destination directory
                chemin_fichier_destination = os.path.join(repertoire_destination,
                                                          os.path.relpath(chemin_fichier, source_dir))

                # Ensure that the destination directory exists
                os.makedirs(os.path.dirname(chemin_fichier_destination), exist_ok=True)

                # Copy the file with its full path to the destination directory
                shutil.copy2(chemin_fichier, chemin_fichier_destination)
                print(f"File copied and processed: {chemin_fichier_destination}")

                file_count += 1
                progress_value = int((file_count / total_files) * 100)
                self.progress_bar.setValue(progress_value)

        # Show the completion message
        self.show_completion_message()

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TextReplacementApp()
    window.show()
    sys.exit(app.exec_())
