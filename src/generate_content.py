import os
from pathlib import Path
from block_markdown import markdown_to_html_node

def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("#"):
            title = line[1:].strip()
            return title
    raise Exception("no header found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as file:
        from_contents = file.read()
     
        with open(template_path) as file:
            template = file.read()

            new_html_node = markdown_to_html_node(from_contents)
            new_html = new_html_node.to_html()
            title = extract_title(from_contents)
            template = template.replace("{{ Title }}", title)
            template = template.replace("{{ Content }}", new_html)


            dest_dir_path = os.path.dirname(dest_path)
            if dest_dir_path != "":
                os.makedirs(dest_dir_path, exist_ok=True)
            to_file = open(dest_path, "w")
            to_file.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        if os.path.isfile(entry_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(entry_path, template_path, dest_path)

        elif os.path.isdir(entry_path):
            generate_pages_recursive(entry_path, template_path, dest_path)


