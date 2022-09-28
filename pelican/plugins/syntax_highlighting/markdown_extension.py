from __future__ import annotations

import shutil
import subprocess

from markdown.core import Markdown
from markdown.extensions import Extension, fenced_code
from markdown.preprocessors import Preprocessor

from .settings import SyntaxHighlightingSettings


def render_code(
    code: str,
    language: str | None,
    settings: SyntaxHighlightingSettings,
) -> str:
    if shutil.which("code2html"):
        cmd = ["code2html"]
    elif shutil.which("npx"):
        cmd = ["npx", "code2html"]
    else:
        raise RuntimeError("Found no way to run code2html")

    cmd += [
        "--backend",
        settings.backend,
        "--class",
        settings.css_class,
        "--linenos-class",
        settings.linenos_class,
        "--wrap-class",
        settings.wrap_class,
        "--input",
        "-",
        "--output",
        "-",
    ]

    if language:
        cmd += ["-l", language]

    if settings.linenos:
        cmd.append("--linenos")

    if settings.wrap:
        cmd.append("--wrap")

    rendered = (
        subprocess.check_output(
            cmd,
            input=code.encode(),
        )
        .decode()
        .strip()
    )
    return rendered


class FencedCodeProcessor(Preprocessor):
    FENCED_BLOCK_RE = fenced_code.FencedBlockPreprocessor.FENCED_BLOCK_RE

    def __init__(self, settings: SyntaxHighlightingSettings, md: Markdown):
        super().__init__(md)
        self.settings = settings

    def run(self, lines: list[str]) -> list[str]:
        text = "\n".join(lines)
        while True:
            m = self.FENCED_BLOCK_RE.search(text)
            if not m:
                break

            lang = m.group("lang")
            code = m.group("code")
            rendered = render_code(code, lang, self.settings)
            text = f"{text[: m.start()]}\n{rendered}\n{text[m.end() :]}"

        return text.split("\n")


class FencedCodeExtension(Extension):
    def __init__(self, settings: SyntaxHighlightingSettings):
        super().__init__()

        self.settings = settings

    def extendMarkdown(self, md: Markdown):
        md.registerExtension(self)
        md.preprocessors.register(
            FencedCodeProcessor(self.settings, md),
            "syntax_highlighting_fenced_code_block",
            200,
        )
