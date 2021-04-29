# A simple blog on things that interest me. 

A hacked together minimal static website generated from JSON files for things that interest me.
Do not use this in production! If you do and the server catches on fire, then it's not my fault.

This is a proof of concept where there are two things that I want to put an emphasis on:
- Minimal dependencies.
- KISS

## Motivation
The goal of this project was to answer the following question:
#### Is it a good idea to have a statically generated webiste that uses JSON files a data source?

This is a very simple and statically generated site. My website https://huynguyen.tech, follows three principles:
- Minimalism
- Simplicity
- Have the least amount of dependencies

This website is used write about things that interest me and as a note keeping application that I can share with other people. If other people are reading my posts, then that is a nice bonus!

## How this works
The project consists of the following directories:
- base: Contains basic building blocks of the website.
- content: Contains the website posts as JSON files.
- images: Contains images that is used in posts.
- posts: Generated posts from json files.

The program (build.py) does follows the following steps:
1. Loads the template files (/base/base.html and /base/post.html).
2. Loop through each JSON file in /content:
3. Convert JSON to HTML and save it in /posts.
4. Create index.html.

Now, to keep the parser not really a transpiler simple each article has the following structure:
```json
{
```

The `in_index` determines if the post should appear in the home page (index.html).

The `image` is the filename of the hero image of the post.

The `title` and `date` is ... I'll leave that as homework for the reader.

Now we just have the `content` left. This one is special, it follows a few simple rules:
1. Each root item in `content` can only contain a single child. That is each dict object in `content` can only contain exactly one of the following keys (tag): `p`, `code`, and `img`.
2. Each of the dict objects (`p`, `code`, and `img`), must have a list as its value.
3. Inside the value you can only have the following objects: a string and a link.
4. A link must follow the following format: `{ "a": [ "url", "text"] }`.

The reason each item in `content` are dict objects is because this gives us the ability to have multiple items with the same key.

As for why we use a list as the values, it gives us the following advantages:
- Allows us to easily add content.
- Concistency, so we don't need to parse each value in a different way.
- We know that we have reach the lowest point in the nested heriarcal structure of `content`.

Notice that `p`, `code`, and `img` represents an HTML paragraph and image.

To parse the `content`, we first run it through a recursive parser.

Why?

Because I rarely get the chance to implement and use such a thing. (In hindsight, a simple nested loops for three layers is much simpler and would of made the implentation much cleaner and simpler!).

This recusive parser converts the `content` into two arrays: `block_ids` (a list of numbers that allows us to tell which block_tag and block_content belong together), `block_tags` (contains a list of tags), and `block_contents`(contains the only string).

If we run the above example, the `block_ids`, `block_tags`, and `block_content` will look as follows:
```
block_ids = [0, 0, 0, 0, 1, 1, 2]
block_tags = [
    ['p'], ['p', 'a'], ['p', 'a'], ['p'],
    ['code'], ['code'],
    ['img']
]
block_content = [
    'Hello World', 'https://www.rust-lang.org/', 'Rust Lang', '.',
    'nano hello_world.rs', 'rustc hello_world.rs',
    'hello_world.jpg'
]
```

Notice that we have the following correlation, `block_ids[n]`, `block_tags[n]`, and `block_content[n]`.



## UNDER CONSTRUCTION
