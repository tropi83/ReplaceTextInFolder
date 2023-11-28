import os
import re
import shutil
from datetime import datetime
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QProgressBar, QPushButton,
    QFileDialog, QLineEdit, QMessageBox, QHBoxLayout, QScrollArea, QCheckBox
)

class TextReplacementApp(QWidget):
    def __init__(self):
        super().__init__()

        self.help_choose_folder = None
        self.help_choose_word_label = None
        self.word_pairs = None
        self.progress_value = None
        self.status_label = None
        self.word_pairs_layout = None
        self.word_pairs_widget = None
        self.scroll_area = None
        self.progress_bar = None
        self.replace_button = None
        self.rename_checkbox = None
        self.add_word_pair_button = None
        self.select_source_button = None
        self.select_destination_button = None
        self.source_path_input = None
        self.destination_path_input = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Project Robber ')
        self.setGeometry(300, 300, 800, 300)

        self.help_choose_word_label = QLabel('Ajouter des chaines de caractères à remplacer (case-sensitive):')
        self.help_choose_folder = QLabel('Choisissez les dossiers sources et destinations')
        self.status_label = QLabel('Status:')
        self.status_label.hide()  # Masquer le label status
        self.word_pairs_layout = QVBoxLayout()

        self.word_pairs_widget = QWidget()
        self.word_pairs_widget.setLayout(self.word_pairs_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.word_pairs_widget)

        self.progress_bar = QProgressBar()
        self.progress_bar.hide()
        self.replace_button = QPushButton('Lancer le traitement')
        self.rename_checkbox = QCheckBox('Renommer aussi les dossiers et fichiers à partir des chaines de caractères '
                                         'à remplacer')
        self.add_word_pair_button = QPushButton('Ajouter une chaine de caractères à remplacer')
        self.select_source_button = QPushButton('Sélectionner le dossier source')
        self.select_destination_button = QPushButton('Sélectionner le dossier de destination')
        self.source_path_input = QLineEdit()
        self.destination_path_input = QLineEdit()

        # Bouton selection dossiers (source et destination)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.source_path_input)
        button_layout.addWidget(self.select_source_button)
        button_layout2 = QHBoxLayout()
        button_layout2.addWidget(self.destination_path_input)
        button_layout2.addWidget(self.select_destination_button)

        layout = QVBoxLayout()
        layout.addWidget(self.help_choose_folder)
        layout.addLayout(button_layout)
        layout.addLayout(button_layout2)
        layout.addWidget(self.help_choose_word_label)
        layout.addWidget(self.scroll_area)
        layout.addWidget(self.add_word_pair_button)
        layout.addWidget(self.rename_checkbox)
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.replace_button)
        self.setLayout(layout)

        self.progress_value = 0
        self.word_pairs = []

        self.replace_button.clicked.connect(self.replace_text)
        self.add_word_pair_button.clicked.connect(self.add_word_pair)
        self.select_source_button.clicked.connect(self.select_source_directory)
        self.select_destination_button.clicked.connect(self.select_destination_directory)

        # Ajouter une paire de chaines de caractères par défaut
        self.add_word_pair()

    def add_word_pair(self):
        word_to_replace_input = QLineEdit()
        new_word_input = QLineEdit()

        word_pair_layout = QHBoxLayout()
        word_pair_layout.addWidget(QLabel('A remplacer:'))
        word_pair_layout.addWidget(word_to_replace_input)
        word_pair_layout.addWidget(QLabel('Par:'))
        word_pair_layout.addWidget(new_word_input)

        self.word_pairs_layout.addLayout(word_pair_layout)
        self.word_pairs.append((word_to_replace_input, new_word_input))

        # Rafraîchir la zone de défilement pour prendre en compte les nouveaux champs
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

    def update_progress(self):
        self.progress_bar.setValue(self.progress_value)

    def show_completion_message(self):
        if self.rename_checkbox.isChecked():
            QMessageBox.information(self, 'Opération finie', 'Dossiers, fichiers et textes dans les fichiers remplacés.')
        else:
            QMessageBox.information(self, 'Opération finie', 'Textes dans les fichiers remplacés.')

    def replace_text(self):
        # Utiliser les valeurs des champs de texte au lieu des dialogues de sélection
        source_dir = self.source_path_input.text()
        if not source_dir or not os.path.exists(source_dir):
            self.status_label.setText('Veuillez sélectionner un dossier source valide.')
            return

        destination_dir = self.destination_path_input.text()
        if not destination_dir or not os.path.exists(destination_dir):
            self.status_label.setText('Veuillez sélectionner un dossier de destination valide.')
            return

        # Afficher la barre de progression
        self.progress_bar.show()
        self.status_label.show()

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
                chemin_fichier = os.path.join(dossier, fichier)

                # Vérifier si le fichier a une extension dans la liste d'exceptions
                if any(fichier.lower().endswith(ext) for ext in files_extensions_ignored):
                    # Copier le fichier sans effectuer de remplacement de texte
                    chemin_fichier_temp = os.path.join(repertoire_destination, os.path.relpath(chemin_fichier, source_dir))
                    os.makedirs(os.path.dirname(chemin_fichier_temp), exist_ok=True)
                    shutil.copy2(chemin_fichier, chemin_fichier_temp)
                    print(f"File copied to temporary directory (exception): {chemin_fichier_temp}")
                else:
                    # Copier le fichier et effectuer le remplacement de texte
                    chemin_fichier_temp = os.path.join(repertoire_destination, os.path.relpath(chemin_fichier, source_dir))
                    os.makedirs(os.path.dirname(chemin_fichier_temp), exist_ok=True)
                    shutil.copy2(chemin_fichier, chemin_fichier_temp)
                    print(f"Original file copied to temporary directory: {chemin_fichier_temp}")

                    # Remplacement de texte dans le fichier
                    self.remplace_texte_dans_fichier(chemin_fichier_temp)

                    file_count += 1
                    progress_value = int((file_count / total_files) * 100)
                    self.progress_value = progress_value
                    self.update_progress()

        # Replacement of text in the temporary directory
        for dossier, sous_dossiers, fichiers in os.walk(repertoire_destination):
            for fichier in fichiers:
                chemin_fichier_temp = os.path.join(dossier, fichier)

                # Vérifier si le fichier a une extension dans la liste d'exceptions
                if not any(fichier.lower().endswith(ext) for ext in files_extensions_ignored):
                    # Remplacement de texte dans le fichier
                    self.remplace_texte_dans_fichier(chemin_fichier_temp)

                    file_count += 1
                    progress_value = int((file_count / total_files) * 100)
                    self.progress_value = progress_value

                    self.update_progress()

        # Renaming files and directories if the checkbox is checked
        if self.rename_checkbox.isChecked():
            total_files_rename = sum(1 for _, _, files in os.walk(repertoire_destination) for _ in files)
            self.rename_files_and_directories_from_word_pairs(repertoire_destination, total_files_rename)

        # Cacher la barre de progression après le traitement
        self.status_label.hide()
        self.progress_bar.hide()

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

    def rename_files_and_directories_from_word_pairs(self, source, total_files_rename):
        try:
            file_count_rename = 0
            for dossier, sous_dossiers, fichiers in os.walk(source):
                for fichier in fichiers:
                    if not fichier.startswith('.') and any(
                            input_widget.text() in fichier for input_widget, _ in self.word_pairs):
                        chemin_fichier = os.path.join(dossier, fichier)
                        nouveau_nom = self.appliquer_replacements(chemin_fichier)
                        nouveau_chemin_fichier = os.path.join(dossier, nouveau_nom)
                        os.rename(chemin_fichier, nouveau_chemin_fichier)

                        file_count_rename += 1
                        progress_value_rename = int((file_count_rename / total_files_rename) * 100)
                        self.progress_value = progress_value_rename
                        self.update_progress()

                for sous_dossier in sous_dossiers:
                    if not sous_dossier.startswith('.') and any(
                            input_widget.text() in sous_dossier for input_widget, _ in self.word_pairs):
                        chemin_sous_dossier = os.path.join(dossier, sous_dossier)
                        nouveau_nom = self.appliquer_replacements(chemin_sous_dossier)
                        nouveau_chemin_sous_dossier = os.path.join(dossier, nouveau_nom)
                        os.rename(chemin_sous_dossier, nouveau_chemin_sous_dossier)

                        file_count_rename += 1
                        progress_value_rename = int((file_count_rename / total_files_rename) * 100)
                        self.progress_value = progress_value_rename
                        self.update_progress()

                # Recursively call the function for subdirectories
                for sous_dossier in sous_dossiers:
                    sous_dossier_path = os.path.join(dossier, sous_dossier)
                    self.rename_files_and_directories_from_word_pairs(sous_dossier_path, total_files_rename)

        except Exception as e:
            print(f"Erreur lors du traitement de {source}: {str(e)}")

    def appliquer_replacements(self, chemin):
        nouveau_nom = os.path.basename(chemin)
        for word_to_replace_input, new_word_input in self.word_pairs:
            word_to_replace = word_to_replace_input.text()
            new_word = new_word_input.text()
            nouveau_nom = nouveau_nom.replace(word_to_replace, new_word)
        return nouveau_nom

    def select_source_directory(self):
        source_dir = QFileDialog.getExistingDirectory(self, 'Select Source Directory')
        if source_dir:
            self.source_path_input.setText(source_dir)
            self.status_label.setText(f'Dossier Source: {source_dir}')

    def select_destination_directory(self):
        destination_dir = QFileDialog.getExistingDirectory(self, 'Select Destination Directory')
        if destination_dir:
            self.destination_path_input.setText(destination_dir)
            self.status_label.setText(f'Dossier de Destination: {destination_dir}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TextReplacementApp()
    window.show()
    sys.exit(app.exec_())
