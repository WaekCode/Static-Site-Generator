import os 
from markdown import markdown_to_html_node,extract_title

def generate_page(from_path, template_path, dest_path,base_path="/"):
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
    page = page.replace('href="/', f'href="{base_path}')
    page = page.replace('src="/', f'src="{base_path}')


    with open(dest_path,'w') as f:
        f.write(page)



def generate_pages_recursive(dir_path_content, template_path, dest_dir_path,base_path="/"):
    for entry in os.listdir(dir_path_content):
        path = os.path.join(dir_path_content, entry)

        if os.path.isdir(path):
            # compute the corresponding subfolder in dest_dir_path
            rel_path = os.path.relpath(path, dir_path_content)
            sub_dest = os.path.join(dest_dir_path, rel_path)
            # recursive call uses the subfolder as the destination
            generate_pages_recursive(path, template_path, sub_dest, base_path)

        else:
            if entry.endswith(".md"):
                rel_file_path = os.path.relpath(path, dir_path_content)
                output_file_path = os.path.join(dest_dir_path, os.path.splitext(entry)[0] + ".html")
                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

                with open(path, 'r') as file:
                    markdown_content = file.read()

                convert = markdown_to_html_node(markdown_content)
                htmlnode = convert.to_html()
                title = extract_title(markdown_content)

                with open(template_path, 'r') as file:
                    template_content = file.read()

                page = template_content.replace("{{ Title }}", title)
                page = page.replace("{{ Content }}", htmlnode)
                page = page.replace('href="/', f'href="{base_path}')
                page = page.replace('src="/', f'src="{base_path}')

                with open(output_file_path, 'w') as f:
                    f.write(page)
