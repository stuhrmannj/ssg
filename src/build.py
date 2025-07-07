from misc_functions import *
import os

def generate_page(from_path, template_path, dest_path):
    # display page generation locations on execute
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # store content in variable f
    with open(from_path, "r", encoding="utf-8") as f:
        content_markdown = f.read()

    # store template in variable t
    with open(template_path, "r", encoding="utf-8") as t:
        template_html = t.read()
    
    # turn content(markdown) into html
    content = markdown_to_html_node(content_markdown).to_html()

    # extract the title from the markdown content
    title = extract_title(content_markdown)

    # replace the title and content in the template
    final_html = template_html.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", content)

    # Make sure the output directory for dest_path exists
    dir_path = os.path.dirname(dest_path)
    if dir_path:  # Prevent issues if dest_path is just a filename
        os.makedirs(dir_path, exist_ok=True)

    # Write the final HTML to dest_path
    with open(dest_path, "w", encoding="utf-8") as out:
        out.write(final_html)

    
    