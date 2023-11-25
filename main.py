import os
import re
import shutil
from datetime import datetime
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QProgressBar, QPushButton, QFileDialog, \
    QLineEdit, QMessageBox, QHBoxLayout, QScrollArea, QCheckBox


class TextReplacementApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Text Replacement Tool')
        self.setGeometry(300, 300, 600, 300)

        self.status_label = QLabel('Status:')
        self.word_pairs_layout = QVBoxLayout()

        self.word_pairs_widget = QWidget()
        self.word_pairs_widget.setLayout(self.word_pairs_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.word_pairs_widget)

        self.progress_bar = QProgressBar()
        self.replace_button = QPushButton('Replace Text')
        self.rename_checkbox = QCheckBox('Rename Files and Directories')
        self.add_word_pair_button = QPushButton('Add Word Pair')

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.scroll_area)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.replace_button)
        layout.addWidget(self.rename_checkbox)
        layout.addWidget(self.add_word_pair_button)
        self.setLayout(layout)

        self.progress_value = 0
        self.word_pairs = []

        self.replace_button.clicked.connect(self.replace_text)
        self.add_word_pair_button.clicked.connect(self.add_word_pair)

        # Ajouter une paire de mots par défaut
        self.add_word_pair()

    def add_word_pair(self):
        word_to_replace_input = QLineEdit()
        new_word_input = QLineEdit()

        word_pair_layout = QHBoxLayout()
        word_pair_layout.addWidget(QLabel('Word to Replace:'))
        word_pair_layout.addWidget(word_to_replace_input)
        word_pair_layout.addWidget(QLabel('New Word:'))
        word_pair_layout.addWidget(new_word_input)

        self.word_pairs_layout.addLayout(word_pair_layout)
        self.word_pairs.append((word_to_replace_input, new_word_input))

        # Rafraîchir la zone de défilement pour prendre en compte les nouveaux champs
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

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

        # Get the current date for the destination folder name
        current_date = datetime.now()
        folder_name = os.path.basename(source_dir) + "_" + current_date.strftime("%d-%m-%y_%Hh-%Mm-%Ss")
        repertoire_destination = os.path.join(destination_dir, folder_name)

        # Create a temporary directory to store original files
        os.makedirs(repertoire_destination, exist_ok=True)

        # Define image file extensions to ignore
        files_extensions_ignored = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.woff2']

        # Calculate the total number of files for progress
        total_files = 0
        for dossier, sous_dossiers, fichiers in os.walk(source_dir):
            for fichier in fichiers:
                if not any(fichier.lower().endswith(ext) for ext in files_extensions_ignored):
                    total_files += 1

        # Copy the original files to the temporary directory
        file_count = 0
        for dossier, sous_dossiers, fichiers in os.walk(source_dir):
            for fichier in fichiers:
                if not any(fichier.lower().endswith(ext) for ext in files_extensions_ignored):
                    chemin_fichier = os.path.join(dossier, fichier)

                    # Create the path of the file in the temporary directory
                    chemin_fichier_temp = os.path.join(repertoire_destination,
                                                       os.path.relpath(chemin_fichier, source_dir))

                    # Ensure that the temporary directory exists
                    os.makedirs(os.path.dirname(chemin_fichier_temp), exist_ok=True)

                    # Copy the original file to the temporary directory
                    shutil.copy2(chemin_fichier, chemin_fichier_temp)
                    print(f"Original file copied to temporary directory: {chemin_fichier_temp}")

                    file_count += 1
                    progress_value = int((file_count / total_files) * 100)
                    self.progress_value = progress_value
                    self.update_progress()

        # Replacement of text in the temporary directory
        for dossier, sous_dossiers, fichiers in os.walk(repertoire_destination):
            for fichier in fichiers:
                chemin_fichier_temp = os.path.join(dossier, fichier)
                self.remplace_texte_dans_fichier(chemin_fichier_temp)

                file_count += 1
                progress_value = int((file_count / total_files) * 100)
                self.progress_value = progress_value

                self.update_progress()

        # Renaming files and directories if the checkbox is checked
        if self.rename_checkbox.isChecked():
            self.rename_files_and_directories_from_word_pairs(repertoire_destination)
            print(f"RENAME FOLDER AND FILE {repertoire_destination}")

        # Show the completion message
        self.show_completion_message()

    def remplace_texte_dans_fichier(self, fichier):
        try:
            with open(fichier, 'r', encoding='utf-8') as file:
                contenu = file.read()
                nouveau_contenu = contenu

                # Replace text logic here
                for word_to_replace_input, new_word_input in self.word_pairs:
                    word_to_replace = word_to_replace_input.text()
                    new_word = new_word_input.text()
                    nouveau_contenu = re.sub(word_to_replace, new_word, nouveau_contenu, flags=re.M)

            with open(fichier, 'w', encoding='utf-8') as file:
                file.write(nouveau_contenu)
        except Exception as e:
            print(f"Erreur lors du traitement de {fichier}: {str(e)}")

    def rename_files_and_directories_from_word_pairs(self, source):
        try:
            for dossier, sous_dossiers, fichiers in os.walk(source):
                for fichier in fichiers:
                    if not fichier.startswith('.') and any(
                            input_widget.text() in fichier for input_widget, _ in self.word_pairs):
                        chemin_fichier = os.path.join(dossier, fichier)
                        nouveau_nom = self.appliquer_replacements(chemin_fichier)
                        nouveau_chemin_fichier = os.path.join(dossier, nouveau_nom)
                        os.rename(chemin_fichier, nouveau_chemin_fichier)
                        print(f"Fichier renommé : {nouveau_chemin_fichier}")

                for sous_dossier in sous_dossiers:
                    if not sous_dossier.startswith('.') and any(
                            input_widget.text() in sous_dossier for input_widget, _ in self.word_pairs):
                        chemin_sous_dossier = os.path.join(dossier, sous_dossier)
                        nouveau_nom = self.appliquer_replacements(chemin_sous_dossier)
                        nouveau_chemin_sous_dossier = os.path.join(dossier, nouveau_nom)
                        os.rename(chemin_sous_dossier, nouveau_chemin_sous_dossier)
                        print(f"Dossier renommé : {nouveau_chemin_sous_dossier}")

                # Recursively call the function for subdirectories
                for sous_dossier in sous_dossiers:
                    sous_dossier_path = os.path.join(dossier, sous_dossier)
                    self.rename_files_and_directories_from_word_pairs(sous_dossier_path)

            self.status_label.setText('Files and directories renamed successfully.')

        except Exception as e:
            print(f"Erreur lors du traitement de {source}: {str(e)}")

    def appliquer_replacements(self, chemin):
        nouveau_nom = os.path.basename(chemin)
        for word_to_replace_input, new_word_input in self.word_pairs:
            word_to_replace = word_to_replace_input.text()
            new_word = new_word_input.text()
            nouveau_nom = nouveau_nom.replace(word_to_replace, new_word)
        return nouveau_nom


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TextReplacementApp()
    window.show()
    sys.exit(app.exec_())
