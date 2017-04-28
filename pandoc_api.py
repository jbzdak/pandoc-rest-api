# coding=utf8
import pathlib
import subprocess
import io
import tempfile

from flask import Flask, request, after_this_request
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

IN_EXTENSIONS = {
    "latex": "tex",
    "markdown": "md",
    "markdown_github": "md",
    "markdown_mmd": "md",
    "markdown_phpextra": "md",
    "markdown_strict": "md",
}

OUTPUT_FILE_EXTENSION_MAPPING = {
    "beamer": "pdf",
    "latex": "pdf",
    "html5": "html",
    "revealjs": "html",
    "markdown": "md",
    "markdown_github": "md",
    "markdown_mmd": "md",
    "markdown_phpextra": "md",
    "markdown_strict": "md",
}


@app.route("/v0/convert/<in_format>/<out_format>", methods=['POST'])
def convert(in_format, out_format):
    if in_format not in ACCEPTED_INPUT_FORMATS:
        return "Invalid infile format", 404
    if out_format not in ACCEPTED_OUTPUT_FORMATS:
        return "Invalid output format", 404

    tempdir = pathlib.Path(tempfile.mkdtemp())

    out_extension = OUTPUT_FILE_EXTENSION_MAPPING.get(out_format, out_format)
    in_extension = IN_EXTENSIONS.get(in_format, "")

    try:
        # import pudb; pudb.set_trace()
        infile = tempdir / "infile.{}".format(in_extension)
        infile.write_bytes(request.stream.read())

        out = tempdir / "{}.{}".format("outfile", out_extension)
        command = ['pandoc', '-f', in_format, '-t', out_format, "-o", out, infile]
        subprocess.check_call(command, cwd=str(tempdir))

    except:
        shutil.rmtree(tempdir)

    @after_this_request
    def remove_files(response):
        shutil.rmtree(tempdir)
        return response

    return send_file(str(out), attachment_filename=str(out.stem)), 200


