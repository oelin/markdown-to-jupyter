"""A markdown to Jupyter converter.

Currently implemented using a state-machine. This doesn't lead to the nicest
looking code but oh well.
"""


import nbformat as nbf
from nbformat.notebooknode import NotebookNode as Notebook


STATE_MARKDOWN = 0
STATE_CODE = 1


def convert(markdown: str) -> Notebook:
    """
    Converts a markdown source string into a Jupyter notebook.

    Parameters
    ---------

    markdown: str

    Returns
    ------

    notebook: Notebook
    """

    lines = markdown.split('\n')
    cells = []
    saved = ''  # Saved lines for the current cell.
    state = STATE_MARKDOWN

    def buffer(line):
        nonlocal saved
        saved += f'{line}\n'

    def flush():
        nonlocal saved

        cell_type = nbf.v4.new_markdown_cell \
            if state == STATE_MARKDOWN \
            else nbf.v4.new_code_cell

        cells.append(cell_type(saved.strip()))
        saved = ''

    for line in lines:
        if state == STATE_MARKDOWN:
            if line.startswith('```'):
                state = STATE_CODE
                flush()

            elif line.startswith('# ') or line.startswith('## ') or line.startswith('### '):
                state = STATE_MARKDOWN
                flush()
                buffer(line)
                flush()

            else:
                buffer(line)

        elif state == STATE_CODE:
            if line.startswith('```'):
                state = STATE_MARKDOWN
                flush()

            else:
                state = STATE_CODE
                buffer(line)

    flush()
    notebook = nbf.v4.new_notebook()
    notebook['cells'] = cells

    return notebook
