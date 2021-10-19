from pelican import Pelican
import pelican.plugins.signals

from .markdown_extension import FencedCodeExtension


def init_syntax(sender: Pelican):
    sender.settings["MARKDOWN"].setdefault("extensions", []).append(
        FencedCodeExtension(),
    )


def register():
    pelican.plugins.signals.initialized.connect(init_syntax)
