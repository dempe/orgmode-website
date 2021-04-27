import os
import shutil
import parser


CONTENT_DIRECTORY = "content"
STATIC_DIRECTORY = "static"
BUILD_DIRECTORY = "_gen"
ORG_EXTENSION = ".org"
HTML_EXTENSION = ".html"


def generate_site():
    if os.path.exists(BUILD_DIRECTORY):
        shutil.rmtree(BUILD_DIRECTORY)
    os.mkdir(BUILD_DIRECTORY)
    copy_and_parse_content_dir()
    copy_static_dir()


def copy_and_parse_content_dir():
    for root, subdirs, files in os.walk(CONTENT_DIRECTORY):
        new_root = root.replace(CONTENT_DIRECTORY, BUILD_DIRECTORY)
        for subdir in subdirs:
            os.mkdir(os.path.join(new_root, subdir))

        for filename in files:
            new_filename = os.path.join(new_root, filename.replace(ORG_EXTENSION, HTML_EXTENSION))
            with open(new_filename, 'w') as file:
                file.write(parser.export_to_html(os.path.join(root, filename)))


def copy_static_dir():
    os.mkdir(os.path.join(BUILD_DIRECTORY, STATIC_DIRECTORY))
    for root, subdirs, files in os.walk(STATIC_DIRECTORY):
        new_root = os.path.join(BUILD_DIRECTORY, root)
        for subdir in subdirs:
            os.mkdir(os.path.join(new_root, subdir))

        for filename in files:
            shutil.copyfile(os.path.join(root, filename), os.path.join(new_root, filename))


generate_site()
