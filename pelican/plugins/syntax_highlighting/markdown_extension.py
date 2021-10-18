import subprocess

from markdown.core import Markdown
from markdown.extensions import Extension, fenced_code
from markdown.preprocessors import Preprocessor


def render_code(code: str, language: str) -> str:
    rendered = (
        subprocess.check_output(
            ["code2html", "-l", language, "-i", "-", "-o", "-"], input=code.encode()
        )
        .decode()
        .strip()
    )
    return rendered


class FencedCodeProcessor(Preprocessor):
    FENCED_BLOCK_RE = fenced_code.FencedBlockPreprocessor.FENCED_BLOCK_RE

    def run(self, lines: list[str]) -> list[str]:
        text = "\n".join(lines)
        while True:
            m = self.FENCED_BLOCK_RE.search(text)
            if not m:
                break

            lang = m.group("lang")
            code = m.group("code")
            rendered = render_code(code, lang)
            text = f"{text[: m.start()]}\n{rendered}\n{text[m.end() :]}"

        return text.split("\n")


class FencedCodeExtension(Extension):
    def extendMarkdown(self, md: Markdown):
        md.registerExtension(self)
        md.preprocessors.register(
            FencedCodeProcessor(md), "syntax_highlighting_fenced_code_block", 200
        )
