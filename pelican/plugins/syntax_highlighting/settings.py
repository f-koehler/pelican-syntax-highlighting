from __future__ import annotations

from pelican import Pelican


class SyntaxHighlightingSettings:
    def __init__(self):
        self.backend = "prism.js"
        self.linenos = True
        self.css_class = "highlight"
        self.linenos_class = "linenos"

    @staticmethod
    def from_settings(pelican: Pelican) -> SyntaxHighlightingSettings:
        obj = SyntaxHighlightingSettings()
        settings = pelican.settings.get("SYNTAX_HIGHLIGHTING", None)

        if settings is None:
            return obj

        obj.backend = settings.get("backend", obj.backend)
        obj.linenos = settings.get("linenos", obj.linenos)
        obj.css_class = settings.get("css_class", obj.css_class)
        obj.linenos_class = settings.get("linenos_class", obj.linenos_class)

        return obj
