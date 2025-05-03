import re
from typing import List, Tuple

class TextReplacementService:
    """
    Service de logique métier pour le remplacement de texte.
    """
    def __init__(self, word_pairs: List[Tuple[str, str]]):
        self.word_pairs = word_pairs

    def replace_in_text(self, text: str) -> str:
        for old, new in self.word_pairs:
            text = re.sub(old, new, text, flags=re.M)
        return text

    def replace_in_file(self, file_path: str) -> None:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            new_content = self.replace_in_text(content)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
        except Exception as e:
            print(f"Erreur lors du traitement de {file_path}: {e}")
