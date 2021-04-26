import os
import shutil

CONTENT_DIRECTORY = "content"
BUILD_DIRECTORY = "_gen"
ORG_EXTENSION = ".org"
HTML_EXTENSION = ".html"


def generate_site():
    if os.path.exists(BUILD_DIRECTORY):
        shutil.rmtree(BUILD_DIRECTORY)
    os.mkdir(BUILD_DIRECTORY)

    for root, subdirs, files in os.walk(CONTENT_DIRECTORY):
        new_root = root.replace(CONTENT_DIRECTORY, BUILD_DIRECTORY)
        for subdir in subdirs:
            os.mkdir(os.path.join(new_root, subdir))

        for filename in files:
            file_content = []
            with open(os.path.join(root, filename), 'r') as file:
                file_content = file.readlines()

            new_filename = os.path.join(new_root, filename.replace(ORG_EXTENSION, HTML_EXTENSION))
            with open(new_filename, 'w') as file:
                file.writelines(file_content)


generate_site()
