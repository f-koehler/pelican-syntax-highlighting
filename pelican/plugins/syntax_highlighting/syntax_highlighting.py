from pelican import Pelican
import pelican.plugins.signals

from .markdown_extension import FencedCodeExtension
from .settings import SyntaxHighlightingSettings


def init_syntax(sender: Pelican):
    settings = SyntaxHighlightingSettings.from_settings(sender)
    sender.settings["MARKDOWN"].setdefault("extensions", []).append(
        FencedCodeExtension(settings),
    )


def register():
    pelican.plugins.signals.initialized.connect(init_syntax)
