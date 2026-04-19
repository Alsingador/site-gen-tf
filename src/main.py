import os
import shutil
import sys

from conversion import *


def main():
    print("started")
    try:
        basepath = sys.argv[1]
    except:
        basepath = "/"
    if not basepath:
        basepath = "/"

    destination = "docs"

    set_up_directory("static", destination)
    pages_created = generate_pages_recursive("content", "template.html", destination, basepath)
    print(pages_created)
    print("done")


def generate_pages_recursive(path, template, dest, basepath):
    if os.path.isfile(path):
        if path.endswith(".md"):
            pub = path.replace(path.split("/")[0], dest, 1) 
            pub = pub.replace(".md", ".html")
            generate_page(path, template, pub, basepath)
            return [pub]
        return []
    mds = []
    for item in os.listdir(path):
        mds = mds + generate_pages_recursive(os.path.join(path,item), template, dest, basepath)
    return mds


def set_up_directory(source, destination):
    if not os.path.exists(source):
        raise Exception(f"Missing source argument: {source}")
    if os.path.exists(destination):
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


def extract_title(markdown):
    for line in markdown.split('\n'):
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No h1 header (# ) in markdown")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"generating page from {from_path} to {dest_path} using {template_path}")
    source_md = ""
    template_html = ""
    with open(from_path, 'r') as f:
        source_md = f.read()
    with open(template_path, 'r') as f:
        template_html = f.read()
    
    source_html = markdown_to_html_node(source_md).to_html()
    title = extract_title(source_md)

    site_html = template_html.replace("{{ Title }}", title)
    site_html = site_html.replace("{{ Content }}", source_html)
    site_html = site_html.replace('href="/', f'href="{basepath}')
    site_html = site_html.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(site_html)




if __name__ == "__main__":
    main()
