import json
import os
import re

# Used to assign an id to each root block in content.
parsed_blocks = []
# Used to keep track of the parent and decendents of each object in content.
parse_stack = []

# A list of ids for each object in content.
block_ids = []
# A list of arrays that contain the parent and decendents for each object in content.
block_tags = []
# A list of text, code, and links.
block_contents = []

index_posts = []

# Run every single object recursively. This essentially runs from outer in inner, 
# top to bottom.
def parse_post(json_object: object) -> None:
    # Run through each item in this dictionary, if an item is a dictionary or list, 
    # run it through this function.
    if type(json_object) is dict:
        for key in json_object:
            value = json_object[key]
            
            if is_json_object_dict_or_list(value):
                # Keep track of the recursion.
                parse_stack.append(str(key))
                parse_post(value)
                parse_stack.pop()

                # Since links can never be a root item in content, 
                # we don't want consider this as a block.
                if str(key) not in ["a"]:
                    parsed_blocks.append(str(key))

    # Run through each item in this list, if an item is a dictionary or list, 
    # run it through this function.
    elif type(json_object) is list:
        for item in json_object:
            if is_json_object_dict_or_list(item):
                parse_post(item)

            # We're at the point were there are not more lists or dictionaries.
            # We can now start to build the content so that we can later use this
            # to build the HTML.
            else:
                tags = []

                # Not sure why block_tags.append(parse_stack) doesn't work.
                for tag in parse_stack:
                    tags.append(tag)

                block_ids.append(len(parsed_blocks))
                block_tags.append(tags)
                block_contents.append(item)


# Return the true if object is a dictionary or list.
def is_json_object_dict_or_list(json_object: object) -> bool:
    if type(json_object) is dict or type(json_object) is list:
        return True
    return False


# Return JSON object from the given path.
def read_file(path: str) -> object:
    with open(path, "r") as file:
        return json.loads(file.read())


# Return the next item in a list. If there is none, return None.
def next(array: list, index: int) -> object:
    if index < len(array) - 1:
        return array[index + 1]
    return None


# Return the previous item in a list. If there is none, return None.
def previous(array: list, index: int) -> object:
    if index > 0:
        return array[index - 1]
    return None


# Return HTML code that is parsed from JSON file that has been broken down
# into block_ids, block_tags, and block_contents.
def create_html() -> str:
    html = ""
    link_stack = []

    for i in range(len(block_tags)):
        # Root ids.
        prev_root_id = previous(block_ids, i)
        root_id = block_ids[i]
        next_root_id = next(block_ids, i)

        # Tags.
        # previous_tags = previous(block_tags, i)
        tags = block_tags[i]
        # next_tags = next(block_tags, i)

        content = block_contents[i]
        next_content = next(block_contents, i)

        root_tag = tags[0]

        # Handle paragraphs and paragraphs with links.
        if root_tag == "p":
            # Handle the start of a paragraph.
            if prev_root_id != root_id and next_root_id == root_id:
                # If we run into a link at the start of the paragraph,
                # make sure the link stack is empty, if it is, then we know
                # this is a new link and not part of a previous link.

                if tags[-1] == "a":
                    html += f'<p><a href="{content}" target="_blank" rel="noreferrer">{next_content}</a>'
                    link_stack.append("a")
                else:
                    html += f"<p>{content}"

            # Handle the middle of the paragraph.
            elif prev_root_id == root_id and next_root_id == root_id:
                # If we run into a link in the middle of the paragraph,
                # make sure the link stack is empty, if it is, then we know
                # this is a new link and not part of a previous link.
                if tags[-1] == "a":
                    if len(link_stack) >= 1:
                        link_stack = []
                        continue
                    else:
                        html += (
                            f'<a href="{content}" target="_blank" rel="noreferrer">{next_content}</a>'
                        )
                        link_stack.append("a")
                # This is just text, just add it without any special tags.
                else:
                    html += f"{content}"

            # Handle the end of a paragraph.
            elif prev_root_id == root_id and next_root_id != root_id:
                # Links are handled when we first encounter it.
                # So when the cursor meets the folowing { [a], a, ... },
                # it handles the following link as well. We can just ignore
                # the link at the end of the paragraph.
                if tags[-1] == "a":
                    html += f"</p>"
                else:
                    html += f"{content}</p>"

            # Handle a paragraph with no links.
            else:
                html += f"<p>{content}</p>"

        # Handle code blocks or single line of code.
        elif root_tag == "code":
            # Handle the start of code with multiple lines.
            if prev_root_id != root_id and next_root_id == root_id:
                html += f'<div class="is-inline-block has-text-weight-light has-background-light p-5 mb-6"><p>{content}</p>'

            # Handle the middle of code with multiple lines.
            elif prev_root_id == root_id and next_root_id == root_id:
                html += f"<p>{content}</p>"

            # Handle the end of code with multiple lines.
            elif prev_root_id == root_id and next_root_id != root_id:
                html += f"<p>{content}</p></div>"

            # Handle the a single line of code.
            else:
                html += f'<div class="is-inline-block has-text-weight-light has-background-light p-5 mb-6"><p>{content}</p></div>'

    return html


# Return a string containing the contents of a file.
def load_file(path: str) -> str:
    with open(path, "r") as file:
        return file.read()


# Transpile a JSON post to HTML.
def create_post(
    base_template: str, post_template: str, content: object, file_name: str
) -> str:
    # Clear globals that is used by the recersive parser.
    global parsed_blocks
    global parse_stack
    global block_ids
    global block_tags
    global block_contents

    parsed_blocks = []
    parse_stack = []
    block_ids = []
    block_tags = []
    block_contents = []

    index_post = post_template.replace(":content:", "")

    # Build the HTML string of a post.
    for item in content:
        item_content = content[item]
        innerHTML = ""

        if item == "image":
            if len(item_content) > 0:
                innerHTML = f'<img src="../images/{item_content}">'
            index_post = index_post.replace(
                ":image:", f'<img src="./images/{item_content}">'
            )

        elif item == "content":
            parse_post(item_content)
            innerHTML = f'<div class="content">{create_html()}</div>'

        elif item == "page":
            base_template = base_template.replace(":page:", item_content)

        elif item == "in_index":
            continue

        else:
            innerHTML = item_content

        post_template = post_template.replace(f":{item}:", innerHTML)
        index_post = index_post.replace(f":{item}:", innerHTML)

    if bool(content["in_index"]):
        index_posts.append(index_post)

    return base_template.replace(":posts:", post_template)


def prepare_base(base: str, index: bool) -> str:
    links_post = {
        ":home:": "../index.html",
        ":resume:": "../base/resume.html",
        ":about:": "./about.html",
        ":css:": "../base/base.css",
        ":js:": "../base/base.js",
        ":apple_icon:": "../apple-touch-icon.png",
        ":32_icon:": "../favicon-32x32.png",
        ":16_icon:": "../favicon-16x16.png",
        ":site_webmanifest:": "../site.webmanifest"
    }
    links_index = {
        ":home:": "./index.html",
        ":page:": "Home",
        ":resume:": "./base/resume.html",
        ":about:": "./posts/about.html",
        ":css:": "./base/base.css",
        ":js:": "./base/base.js",
        ":apple_icon:": "./apple-touch-icon.png",
        ":32_icon:": "./favicon-32x32.png",
        ":16_icon:": "./favicon-16x16.png",
        ":site_webmanifest:": "./site.webmanifest"
    }
    links = links_post

    if index:
        links = links_index

    for key in links:
        base = base.replace(f"{key}", links[key])

    return base


def main() -> None:
    content_path = "content"

    base_template_posts = prepare_base(load_file("base/base.html"), False)
    base_template_index = prepare_base(load_file("base/base.html"), True)
    post_template = load_file("base/post.html")

    # Create posts.
    for filename in os.listdir(content_path):
        if filename.endswith(".json"):
            path = os.path.join(content_path, filename)
            post = read_file(path)
            post_path = filename.replace(".json", ".html")

            with open(os.path.join("posts", post_path), "w") as file:
                file.write(
                    create_post(base_template_posts, post_template, post, post_path)
                )

            if bool(post["in_index"]):
                index_posts[-1] = index_posts[-1].replace(
                    "card m-3", "card m-3 grow is-clickable"
                )
                index_posts[-1] = f'<a href="./posts/{post_path}">{index_posts[-1]}</a>'

    with open("index.html", "w") as file:
        html = base_template_index.replace(":posts:", "".join(index_posts))
        file.write(html)


main()