import os
import shutil
from typing import List

class FileManager:
    """
    Service pour la gestion des fichiers : copie et filtrage par extension.
    """
    def __init__(self, ignored_extensions: List[str]):
        self.ignored_extensions = ignored_extensions

    def is_ignored(self, filename: str) -> bool:
        return any(filename.lower().endswith(ext) for ext in self.ignored_extensions)

    def count_eligible_files(self, root: str) -> int:
        count = 0
        for _, _, files in os.walk(root):
            count += sum(1 for f in files if not self.is_ignored(f))
        return count

    def copy_all(self, src: str, dest: str) -> None:
        for folder, _, files in os.walk(src):
            for f in files:
                src_path = os.path.join(folder, f)
                rel_path = os.path.relpath(src_path, src)
                dest_path = os.path.join(dest, rel_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(src_path, dest_path)
