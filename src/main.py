from textnode import *
import shutil
import os
from block_markdown import *

def main():
    copy_source_to_destination("src/static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")



    

def copy_source_to_destination(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
        os.mkdir(destination)

    for content in os.listdir(source):
        source_path = os.path.join(source, content)
        destination_path = os.path.join(destination, content)
        print(f"Copying {source_path} to {destination_path}")

        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
        elif os.path.isdir(source_path):
            if not os.path.exists(destination_path):
                os.mkdir(destination_path)
            copy_source_to_destination(source_path, destination_path)
        

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
            template_contents = file.read()

            new_html_node = markdown_to_html_node(from_contents)
            new_html = new_html_node.to_html()
            title = extract_title(from_contents)
            filled_template = template_contents.replace("{{ Title }}", title)
            filled_template = filled_template.replace("{{ Content }}", new_html)

            if not os.path.exists(os.path.dirname(dest_path)):
                os.makedirs(os.path.dirname(dest_path))
            with open(dest_path, 'w') as file:
                file.write(filled_template)

    
    





if __name__ == '__main__':
    main()