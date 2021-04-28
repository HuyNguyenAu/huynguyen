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

This website is used write about things that interest me and as a note keeping application that I can share with other people. If other people are reading my articles, then that is a nice bonus!

## How this works
The project consists of the following directories:
- base: Contains basic building blocks of the website.
- content: Contains the website articles as JSON files.
- images: Contains images that is used in articles.
- posts: Generated articles from json files.

The program (build.py) does follows the following steps:
1. Loads the template files (/base/base.html and /base/post.html).
2. Loop through each JSON file in /content:
3. Convert JSON to HTML and save it in /posts.
4. Create index.html.

Now, to keep the parser not really a transpiler simple the article has the following structure:
```json
{
    "in_index": 1,
    "image": "building_element_desktop_on_solus.jpg",
    "title": "Building Element Desktop From Source On Solus",
    "date": "24/03/2020",
    "content": [
        {
            "p": [
                "Hello World",
                {
                    "a": [
                        "https://huynguyen.tech",
                        "huynguyen.tech"
                    ]
                },
                "."
            ]
        },
        {
            "code": [
                "nano hello_world.rs",
                "rustc hello_world.rs"
            ]
        },
         {
            "img": [
                "hello_world.jpg",
            ]
        },
    ]
}
```

