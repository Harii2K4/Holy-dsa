import os
import shutil
from md_to_html_nodes import md_to_html_nodes


def copy_static_to_public(src_dir: str, dest_dir: str):

    for item in os.listdir(src_dir):
        curr_src_path = os.path.join(src_dir, item)
        curr_dest_path = os.path.join(dest_dir, item)
        if os.path.isdir(curr_src_path):
            print(f"Copying dir :{curr_src_path}")
            os.mkdir(curr_dest_path)
            copy_static_to_public(curr_src_path, curr_dest_path)
        else:
            print(f"copying file :{curr_src_path}")
            shutil.copy(curr_src_path, curr_dest_path)


def extract_title(md: str) -> str:
    lines = md.strip(" ").strip("\n").split("\n")
    if not lines:
        raise Exception("Empty markdown")
    for line in lines:
        if not line:
            continue
        if not line[0] == "#":
            raise Exception("Start the markdown with a h1 header")
        else:
            if line[1] != " ":
                raise Exception(f"leave a space after # to get title: {line}")

            return line[2:]

    raise Exception("Start the markdown with a h1 header")


def build_site(src_path: str, dest_path: str, template_content: str):

    for item in os.listdir(src_path):
        curr_src_path = os.path.join(src_path, item)

        if os.path.isdir(curr_src_path):
            print(f"Making dir :{curr_src_path}")
            curr_dest_path = os.path.join(dest_path, item)
            os.mkdir(curr_dest_path)
            build_site(curr_src_path, curr_dest_path, template_content)
        else:
            if not item.endswith(".md"):
                print(f"The file is not md so cant convert: {curr_src_path}")
                continue

            print(f"Converting file to html :{curr_src_path}")
            new_name = item[:-2] + "html"
            curr_dest_path = os.path.join(dest_path, new_name)
            with open(curr_src_path, "r") as f:
                content = f.read()

            title = extract_title(content)
            div_object = md_to_html_nodes(content)
            file_content = template_content.format(
                Title=title, Content=div_object.to_html()
            )
            with open(curr_dest_path, "w") as f:
                print(f"Write file content :{curr_dest_path}")
                f.write(file_content)


def main():
    curr_dir = os.getcwd()

    # Deleting the contents of public
    print("----------Deleting-----------")
    public_dir = os.path.join(curr_dir, "public")
    for item in os.listdir(public_dir):
        curr_path = os.path.join(public_dir, item)
        if os.path.isdir(curr_path):
            print(f"Deleting dir :{curr_path}")
            shutil.rmtree(curr_path)
        else:
            print(f"Deleting file :{curr_path}")
            os.remove(curr_path)

    # copying static into public

    print("----------Copying-----------")
    static_dir = os.path.join(curr_dir, "static")
    copy_static_to_public(static_dir, public_dir)

    # create the static site
    content_dir = os.path.join(curr_dir, "src", "content")
    template_path = os.path.join(curr_dir, "template.html")

    with open(template_path, "r") as f:
        template_content = f.read()

    print("----------Building Site-----------")
    build_site(content_dir, public_dir, template_content)
    print("----------Starting Server-----------")


if __name__ == "__main__":
    # print(extract_title("#this is the title"))
    main()
