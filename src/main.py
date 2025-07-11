import os
import shutil
from build import *
import sys

def copy_recursive(src, dst):
    for entry in os.listdir(src):
        src_entry_path = os.path.join(src, entry)
        dst_entry_path = os.path.join(dst, entry)
        print(dst_entry_path)
        if os.path.isfile(src_entry_path):
            shutil.copy(src_entry_path, dst_entry_path)
        elif os.path.isdir(src_entry_path):
            os.mkdir(dst_entry_path)
            copy_recursive(src_entry_path,dst_entry_path)

def main():
    # identifies the directory this file is run from
    src_dir = os.path.dirname(os.path.abspath(__file__))

    # identifies the directory one level up, where docs should be
    docs_dir = os.path.join(src_dir, "..", "docs")

    # identifies the static directory, also one level up
    static_dir = os.path.join(src_dir, "..", "static")

    # check if docs exists, and if it does, delete it
    if os.path.exists(docs_dir):
        shutil.rmtree(docs_dir)

    # create a new docs directory
    os.mkdir(docs_dir)

    # call the copy function to copy entire static directory into the docs directory
    copy_recursive(static_dir, docs_dir)

    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    project_root = os.path.join(src_dir, "..")

    content_md = os.path.join(project_root, "content")
    template_html = os.path.join(project_root, "template.html")
    docs_html = os.path.join(project_root, "docs")
    
    generate_pages_recursive(content_md, template_html, docs_html, basepath)

if __name__ == "__main__":
    main()