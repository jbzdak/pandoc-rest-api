# coding=utf8
import pathlib
import subprocess
import io
import tempfile

from flask import Flask, request
from flask.helpers import send_file
from pip._vendor.distlib._backport import shutil

app = Flask(__name__)

__ACCEPTED_FORMATS_STR = """docbook, haddock, html, json, latex, markdown, markdown_github,
markdown_mmd, markdown_phpextra, markdown_strict, mediawiki,
native, opml, org, rst, textile"""

ACCEPTED_INPUT_FORMATS = {
    format.strip()
    for format in __ACCEPTED_FORMATS_STR.strip().split(",")
}

__ACCEPTED_OUTPUT_FORMATS_STR = """
asciidoc, beamer, context, docbook, docx, dzslides, epub, epub3,
fb2, html, html5, icml, json, latex, man, markdown,
markdown_github, markdown_mmd, markdown_phpextra,
markdown_strict, mediawiki, native, odt, opendocument, opml,
org, plain, revealjs, rst, rtf, s5, slideous, slidy,
texinfo, textile
"""

ACCEPTED_OUTPUT_FORMATS = {
    format.strip()
    for format in __ACCEPTED_OUTPUT_FORMATS_STR.strip().split(",")
}

OUTPUT_FILE_EXTENSION_MAPPING = {
    "beamer": "pdf",
    "latex": "pdf",
    "html5": "html",
    "revealjs": "html",
    "markdown_github": "md",
    "markdown_mmd": "md",
    "markdown_phpextra": "md",
    "markdown_strict": "md",
}


INPUT_CONTENTS_ATTR = "data"


@app.route("/convert/<in_format>/<out_format>")
def convert(in_format, out_format):
    if in_format not in ACCEPTED_INPUT_FORMATS:
        return "Invalid infile format", 404
    if out_format not in ACCEPTED_OUTPUT_FORMATS:
        return "Invalid output format", 404
    if request.method != "POST":
        return "Invalid method", 405
    if INPUT_CONTENTS_ATTR not in request.form:
        return "Invalid request", 400

    tempdir = pathlib.Path(tempfile.mkdtemp())

    out_extension = OUTPUT_FILE_EXTENSION_MAPPING.get(out_format, out_format)

    try:
        infile = tempdir / "infile"
        infile.write_bytes(request.form[INPUT_CONTENTS_ATTR])

        out = tempdir / "{}.{}".format("outfile", out_extension)
        subprocess.check_call(['pandoc', '-f', in_format, '-t', out_format, "-O", out, infile], cwd=str(tempdir))
        result = io.BytesIO(out.read_bytes())
    finally:
        shutil.rmtree(str(tempdir))

    return send_file(result), 200


if __name__ == "__main__":
    app.run()
