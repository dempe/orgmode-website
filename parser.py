from bs4 import BeautifulSoup as bs
import re

H6 = "****** "
H5 = "***** "
H4 = "**** "
H3 = "*** "
H2 = "** "
H1 = "* "
BEGIN_CODE_BLOCK = "#+begin_src"
END_CODE_BLOCK = "#+end_src"
ORG_COMMENT = "#"
ORG_LIST = "+"
ORG_FILE_EXTENSION = ".org"
HTML_FILE_EXTENSION = ".html"

inside_code_block = False
inside_list = False


def export_to_html(org_filename: str) -> str:
    """
    This function takes an org-mode file and exports it to HTML
    :param org_filename: org-mode file to translate
    :return: a string containing the translated HTML
    """
    if not org_filename.endswith(ORG_FILE_EXTENSION):
        raise Exception(f'{org_filename} is not an org file. Must provide an org-mode file.')

    output_lines = []
    title, language, date, tags, author, description = "", "", "", "", "", ""
    with open(org_filename, 'r') as input:
        for line in input:
            if line.startswith("\n"):
                continue

            output_lines.append(translate_to_html(line))

    return bs("".join(output_lines), "html.parser").prettify()


def translate_to_html(line: str) -> str:
    line = line.replace("\n", "").strip()
    line = translate_block_elements(line)  # must come _before_ following code

    # Don't want to apply formatting to code
    if inside_code_block:
        return line

    return translate_inline_elements(line)


def translate_block_elements(line: str) -> str:
    # Translate headings
    # NOTE: these are order-dependent
    if line.startswith(H6):
        return f'<h6>{line[7:]}</h6>'
    if line.startswith(H5):
        return f'<h5>{line[6:]}</h5>'
    if line.startswith(H4):
        return f'<h4>{line[5:]}</h4>'
    if line.startswith(H3):
        return f'<h3>{line[4:]}</h3>'
    if line.startswith(H2):
        return f'<h2>{line[3:]}</h2>'
    if line.startswith(H1):
        return f'<h1>{line[2:]}</h1>'

    # Rudimentary parsing of code blocks
    # Handle proper syntax highlighting later
    global inside_code_block
    if line.startswith(BEGIN_CODE_BLOCK):
        inside_code_block = True
        return "<pre><code>"
    if line.startswith(END_CODE_BLOCK):
        inside_code_block = False
        return "</code></pre>"

    global inside_list
    if line.startswith(ORG_LIST):
        # Remove the initial "+ "
        line = f'<ul><li>{line[2:]}</li>' if not inside_list else f'<li>{line[2:]}</li>'
        inside_list = True
        return line
    else:
        if inside_list:
            line = f'</ul>{line}'
            inside_list = False

    # Handle comments
    if line.startswith(ORG_COMMENT):
        return ""

    # Default to <p>
    return f'{line}\n' if inside_code_block else "<p>" + line + "</p>"


def translate_inline_elements(line: str) -> str:
    # Use positive lookbehind for spaces.
    # "a_thing_" should NOT match, but "a _thing_" should match.
    line = re.sub("(?<= )/(.*?)/", "<em>\\1</em>", line)
    line = re.sub("(?<= )\\*(.*?)\\*", "<strong>\\1</strong>", line)
    line = re.sub("(?<= )_(.*?)_", "<u>\\1</u>", line)
    line = re.sub("(?<= )~(.*?)~", "<code>\\1</code>", line)
    line = re.sub("(?<= )=(.*?)=", "<samp>\\1</samp>", line)
    line = re.sub("(?<= )\\+(.*?)\\+", "<del>\\1</del>", line)
    line = re.sub(r"\[\[(.*?)]\[(.*?)]]", r"<a href=\1>\2</a>", line)

    return line
