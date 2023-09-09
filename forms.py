from fastapi import Form

def NewsForm(code):
    id = Form(...)
    title = Form(...)
    description = Form(...)
    category_id = Form(...)
    author_id = Form(...)

    return {
        "id": id,
        "title": title,
        "description": description,
        "category_id": category_id,
        "author_id": author_id,
    }