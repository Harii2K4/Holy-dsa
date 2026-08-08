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
            print(f"copying file :{os.path.join(src_dir, item)}")
            shutil.copy(os.path.join(src_dir, item), os.path.join(dest_dir, item))


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

    index_file_md = os.path.join(content_dir, "index.md")

    with open(index_file_md, "r") as f:
        content = f.read()

    title = extract_title(content)
    div_object = md_to_html_nodes(content)
    file_content = template_content.format(Title=title, Content=div_object.to_html())

    # save the file
    dest_path = os.path.join(public_dir, "index.html")
    with open(dest_path, "w") as f:
        print(f"Write file content :{dest_path}")
        f.write(file_content)

    # public_dir = os.path.join(curr_dir, "public")


if __name__ == "__main__":
    # print(extract_title("#this is the title"))
    main()
