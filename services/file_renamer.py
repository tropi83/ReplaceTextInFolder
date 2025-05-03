import os
from typing import List, Tuple, Callable

class FileRenamer:
    """
    Service pour renommer fichiers et dossiers selon des paires de mots.
    """
    def __init__(self, word_pairs: List[Tuple[str, str]]):
        self.word_pairs = word_pairs

    def apply_renames(self, path: str) -> str:
        dirname = os.path.dirname(path)
        basename = os.path.basename(path)
        for old, new in self.word_pairs:
            basename = basename.replace(old, new)
        return os.path.join(dirname, basename)

    def rename_all(self, root: str, progress_callback: Callable[[], None] = None) -> None:
        # Parcours bottom-up pour renommer d'abord les fichiers puis les dossiers
        for folder, subfolders, files in os.walk(root, topdown=False):
            for f in files:
                self._rename(os.path.join(folder, f), progress_callback)
            for sub in subfolders:
                self._rename(os.path.join(folder, sub), progress_callback)

    def _rename(self, path: str, progress_callback: Callable[[], None] = None) -> None:
        new_path = self.apply_renames(path)
        if new_path != path:
            os.rename(path, new_path)
        if progress_callback:
            progress_callback()
