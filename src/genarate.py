import os 
from markdown import markdown_to_html_node,extract_title

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')

    #reading the markdown file 
    with open(from_path, 'r') as file:
        markdown_content = file.read()
    

    convert = markdown_to_html_node(markdown_content)
    htmlnode = convert.to_html()
    title = extract_title(markdown_content)


    #reading the template file 
    with open(template_path, 'r') as file:
        template_content = file.read()  
        
    page = template_content.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", htmlnode)

    with open(dest_path,'w') as f:
        f.write(page)



def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        path = os.path.join(dir_path_content, entry)

        if os.path.isdir(path):
            # compute the corresponding subfolder in dest_dir_path
            rel_path = os.path.relpath(path, dir_path_content)
            sub_dest = os.path.join(dest_dir_path, rel_path)
            # recursive call uses the subfolder as the destination
            generate_pages_recursive(path, template_path, sub_dest)
        else:
            if entry.endswith(".md"):
                print(f'Found file: {path}')
                print(f'Generating page from {path} to {dest_dir_path} using {template_path}')

                # 1. Read the markdown file
                with open(path, 'r') as file:
                    markdown_content = file.read()

                # 2. Convert Markdown to HTML
                convert = markdown_to_html_node(markdown_content)
                htmlnode = convert.to_html()

                # 3. Extract title
                title = extract_title(markdown_content)

                # 4. Read the template file
                with open(template_path, 'r') as file:
                    template_content = file.read()

                # 5. Replace placeholders
                page = template_content.replace("{{ Title }}", title)
                page = page.replace("{{ Content }}", htmlnode)

                # 6. Compute output file path in the current subfolder
                output_file_path = os.path.join(dest_dir_path, os.path.splitext(entry)[0] + ".html")

                # Ensure folder exists
                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

                # 7. Write HTML file
                with open(output_file_path, 'w') as f:
                    f.write(page)

                print(f"✅ Generated {output_file_path}")
