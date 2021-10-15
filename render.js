const { Command, Option } = require("commander");

const program = new Command("render");
program.description("Renders source code files to HTML.")

program
    .addOption(new Option("-b, --backend", "rendering backend to use")
        .choices(["prism.js", "highlight.js", "pygments"])
        .default("highlight.js"))
    .addOption(new Option("-i, --input", "input file, \"-\" for STDIN")
        .default("-"))
    .addOption(new Option("-o, --output", "output file, \"-\" for STDOUT")
        .default("-"))
    .addOption(new Option("-l, --language", "programming language used"));

program.parse(process.argv);

function readSourceCode() { }
function writeRenderedHTML() { }
function renderCode() { }
function renderCodeHighlightJS() {
    const hljs = require("highlight.js/lib/core");
    hljs.registerLanguage("python", require("highlight.js/lib/languages/python"));
    const renderedHTML = hljs.highlight("print('Hello World!')", { language: "python" }).value;
    console.log(renderedHTML);
}
function renderCodePrismJS() { }

renderCodeHighlightJS();
