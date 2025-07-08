from misc_functions import *
import os

def generate_page(from_path, template_path, dest_path, basepath):
    # display page generation locations on execute
    print(f"Generating page from {from_path} to {dest_path} using {template_path} and {basepath}")
    
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

    # add basepath
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')

    # Make sure the output directory for dest_path exists
    dir_path = os.path.dirname(dest_path)
    if dir_path:  # Prevent issues if dest_path is just a filename
        os.makedirs(dir_path, exist_ok=True)

    # Write the final HTML to dest_path
    with open(dest_path, "w", encoding="utf-8") as out:
        out.write(final_html)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    # Get all items in the content directory
    items = os.listdir(dir_path_content)

    print(f"Found items: {items}")

    for item in items:
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path) and item.endswith(".md"):
            item_html = item.replace(".md", ".html")
            dest_path = os.path.join(dest_dir_path, item_html)
            generate_page(item_path, template_path, dest_path, basepath)
        elif os.path.isdir(item_path):
            dest_path = os.path.join(dest_dir_path, item)
            generate_pages_recursive(item_path, template_path, dest_path, basepath)


    
    