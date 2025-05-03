import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QProgressBar, QPushButton,
    QFileDialog, QLineEdit, QMessageBox, QHBoxLayout, QScrollArea, QCheckBox, QWidgetItem
)
from PyQt5.QtCore import Qt

from services.text_replacement_service import TextReplacementService
from services.file_manager import FileManager
from services.file_renamer import FileRenamer
from models.word_pair import WordPair
from utils.progress_tracker import ProgressTracker

class TextReplacementApp(QWidget):
    """
    UI pour sélectionner les dossiers, définir les paires de remplacement
    et lancer le traitement. Avec suppression d'inputs et génération robuste de variantes.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Project Robber')
        self.setGeometry(300, 300, 800, 600)

        # Sélecteurs de dossiers
        self.source_input = QLineEdit()
        self.dest_input = QLineEdit()
        self.select_src_btn = QPushButton('Sélectionner le dossier source')
        self.select_dest_btn = QPushButton('Sélectionner le dossier de destination')

        # Zone scroll pour les paires
        self.word_pairs_layout = QVBoxLayout()
        pairs_widget = QWidget()
        pairs_widget.setLayout(self.word_pairs_layout)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(pairs_widget)

        # Boutons et indicateurs
        self.add_pair_btn = QPushButton('Ajouter une paire de remplacement')
        self.generate_variants_btn = QPushButton('Générer variantes de casse')
        self.rename_checkbox = QCheckBox('Renommer aussi les dossiers et fichiers')
        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.hide()
        self.status_label = QLabel()
        self.status_label.hide()
        self.run_btn = QPushButton('Lancer le traitement')

        # Initialisation de l'UI
        self._init_ui()

    def _init_ui(self):
        # Layout dossiers
        src_layout = QHBoxLayout()
        src_layout.addWidget(self.source_input)
        src_layout.addWidget(self.select_src_btn)

        dest_layout = QHBoxLayout()
        dest_layout.addWidget(self.dest_input)
        dest_layout.addWidget(self.select_dest_btn)

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel("Choisissez les dossiers sources et destination"))
        main_layout.addLayout(src_layout)
        main_layout.addLayout(dest_layout)
        main_layout.addWidget(QLabel("Ajouter des chaînes de remplacement (case-sensitive)"))
        main_layout.addWidget(self.scroll_area)
        main_layout.addWidget(self.add_pair_btn)
        main_layout.addWidget(self.generate_variants_btn)
        main_layout.addWidget(self.rename_checkbox)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.run_btn)
        self.setLayout(main_layout)

        # Connexions
        self.select_src_btn.clicked.connect(self._choose_source)
        self.select_dest_btn.clicked.connect(self._choose_destination)
        self.add_pair_btn.clicked.connect(lambda: self._add_word_pair())
        self.generate_variants_btn.clicked.connect(self._generate_variants)
        self.run_btn.clicked.connect(self._run)

        # Liste des widgets de paires
        self.pair_widgets = []  # list of tuples (container, old_input, new_input)
        # Un premier champ par défaut
        self._add_word_pair()

    def _choose_source(self):
        path = QFileDialog.getExistingDirectory(self, "Select Source Directory")
        if path:
            self.source_input.setText(path)

    def _choose_destination(self):
        path = QFileDialog.getExistingDirectory(self, "Select Destination Directory")
        if path:
            self.dest_input.setText(path)

    def _add_word_pair(self, old_text: str = "", new_text: str = ""):
        """
        Ajoute une paire de QLineEdit pré-remplie si old_text/new_text sont fournis.
        Ajoute également un bouton de suppression pour retirer la paire.
        """
        old_input = QLineEdit()
        old_input.setText(old_text)
        new_input = QLineEdit()
        new_input.setText(new_text)
        delete_btn = QPushButton('Supprimer')
        delete_btn.setFixedWidth(80)

        layout = QHBoxLayout()
        layout.addWidget(QLabel("À remplacer:"))
        layout.addWidget(old_input)
        layout.addWidget(QLabel("Par:"))
        layout.addWidget(new_input)
        layout.addWidget(delete_btn)

        container = QWidget()
        container.setLayout(layout)
        self.word_pairs_layout.addWidget(container)

        self.pair_widgets.append((container, old_input, new_input))

        # Connexion du bouton supprimer
        delete_btn.clicked.connect(lambda: self._remove_word_pair(container))

        # Scroller en bas
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )

    def _remove_word_pair(self, container: QWidget):
        """Supprime le widget container et la paire associée."""
        # Retirer de la liste
        self.pair_widgets = [pw for pw in self.pair_widgets if pw[0] != container]
        # Retirer le widget de layout
        for i in range(self.word_pairs_layout.count()):
            item = self.word_pairs_layout.itemAt(i)
            if isinstance(item, QWidgetItem) and item.widget() == container:
                self.word_pairs_layout.takeAt(i)
                break
        container.deleteLater()

    def _generate_variants(self):
        """
        Génère pour chaque paire actuelle ses variantes de casse:
        original, lower(), upper(), sans doublons.
        Remplace les entrées actuelles par l'ensemble généré.
        """
        # Extraire paires existantes
        base_pairs = []
        for _, old_input, new_input in self.pair_widgets:
            o, n = old_input.text().strip(), new_input.text().strip()
            if o:
                base_pairs.append((o, n))

        # Générer variants
        variants = set()
        for o, n in base_pairs:
            variants.add((o, n))
            variants.add((o.lower(), n.lower()))
            variants.add((o.upper(), n.upper()))

        # Réinitialiser les champs
        for container, *_ in self.pair_widgets:
            container.setParent(None)
        self.pair_widgets.clear()

        # Ajouter chaque variante
        for o, n in sorted(variants):
            self._add_word_pair(o, n)

    def _show_error(self, msg: str):
        QMessageBox.critical(self, "Erreur", msg)

    def _run(self):
        source = self.source_input.text().strip()
        dest = self.dest_input.text().strip()
        if not os.path.isdir(source):
            return self._show_error("Veuillez sélectionner un dossier source valide.")
        if not os.path.isdir(dest):
            return self._show_error("Veuillez sélectionner un dossier de destination valide.")

        # Récupérer les paires validées par l'utilisateur
        pairs = []
        for _, old_input, new_input in self.pair_widgets:
            o, n = old_input.text().strip(), new_input.text().strip()
            if o:
                pairs.append((o, n))
        if not pairs:
            return self._show_error("Ajoutez au moins une paire de remplacement.")

        # Créer le dossier de destination avec timestamp
        stamp = datetime.now().strftime("%d-%m-%y_%Hh-%Mm-%Ss")
        folder_name = f"{os.path.basename(source)}_{stamp}"
        target = os.path.join(dest, folder_name)
        os.makedirs(target, exist_ok=True)

        # Initialisation des services
        fm = FileManager(ignored_extensions=['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.woff2'])
        total_files = fm.count_eligible_files(source)

        # Copie initiale
        self.status_label.setText("Copie des fichiers en cours...")
        self.status_label.show()
        self.progress_bar.setValue(0)
        self.progress_bar.show()
        fm.copy_all(source, target)

        # Tracker de progression
        def update_progress(pct):
            self.progress_bar.setValue(pct)

        tracker = ProgressTracker(total_files, update_progress)
        replacer = TextReplacementService(pairs)

        # Remplacement de texte
        self.status_label.setText("Remplacement du texte dans les fichiers...")
        for root, _, files in os.walk(target):
            for f in files:
                if not fm.is_ignored(f):
                    replacer.replace_in_file(os.path.join(root, f))
                    tracker.advance()

        # Renommage si coché
        if self.rename_checkbox.isChecked():
            renamer = FileRenamer(pairs)
            total_rename = sum(len(f) + len(d) for _, d, f in os.walk(target))
            tracker_ren = ProgressTracker(total_rename, update_progress)
            self.status_label.setText("Renommage des fichiers et dossiers...")
            renamer.rename_all(target, progress_callback=tracker_ren.advance)

        # Fin
        self.progress_bar.hide()
        self.status_label.hide()
        QMessageBox.information(self, "Terminé", "Traitement terminé avec succès.")
