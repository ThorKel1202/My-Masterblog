from flask import Flask, render_template, request, redirect, url_for
import json


app = Flask(__name__)


def load_posts():
    """
        Help-function to load and read the JSON file and return a list of dictionaries of all posts
    """
    
    with open("blog_data.json", "r", encoding="utf-8") as file:
        return json.load(file)
    

def save_posts(posts):
    """
        Help-function that gets the new or updated data for the JSON file and writes the new JSON file
    """
    
    with open("blog_data.json", "w", encoding="utf-8") as file:
        json.dump(posts, file, indent=4, ensure_ascii=False)
        
        
def fetch_post_by_id(post_id):
    """
        Help-function loads the current data from help-function load_posts and search for a given post_id.
        After that it returns the corresponding post or None, if no corresponding post was found.
    """
    
    posts = load_posts()
    for post in posts:
        if post["id"] == post_id:
            return post
    return None
        

@app.route('/')
def index():
    """
        Function loads a list of dictionaries of all posts via help-function load_posts,
        then returns impulse to render jinja2 template via flask which shows all existing posts.
    """
    
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
        Function calls a form to add new post in add.html and takes the new data. Then loads a list of dictionaries
        of all posts via help-function load_posts, then sets a new ID and appends all new data to the existing posts.
        After that it gives the new data to the help-function save_posts to update the JSON file.
        Finally, it returns to the index page.
    """
    
    if request.method == 'POST':
        # Takes new data from form
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # Load existing posts from JSON file via load_posts function
        posts = load_posts()

        # First looking for the next ID, then adds the new post to the existing data
        if posts:
            new_id = max(post["id"] for post in posts) + 1
        else:
            new_id = 1
        
        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content,
            "likes": 0
        }
        
        posts.append(new_post)

        # Saves new data to JSON file via save_posts function
        save_posts(posts)

        # Back to index page
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """
        Function loads a list of dictionaries of all posts via help-function load_posts,
        with list comprehension it compares all posts which have not the given post_id and
        copies them to a new list (of dictionaries). After that it gives the new data to the
        help-function save_posts to update the JSON file. Finally, it returns to the updated index page.
    """
    
    # Load existing posts from JSON file via load_posts function
    posts = load_posts()
    
    # Deletes post with selected ID
    posts = [post for post in posts if post["id"] != post_id]

    # Saves new data to JSON file via save_posts function
    save_posts(posts)

    # Back to index page
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
        Function loads a list of dictionaries of all posts via help-function load_posts,
        and loads a single post of the given post_id from the helper-function fetch_post_by_id.
        It renders the update.html with filled text fields for update them by the user. After that
        it gives the new data to the help-function save_posts to update the JSON file.
        Finally, it returns to the updated index page.
    """
    
    posts = load_posts()
    post = fetch_post_by_id(post_id)

    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        # read data from form
        title = request.form.get('title')
        content = request.form.get('content')
        author = request.form.get('author')

        # updates post
        for p in posts:
            if p["id"] == post_id:
                p["title"] = title
                p["content"] = content
                p["author"] = author
                break

        # Saves new data to JSON file via save_posts function
        save_posts(posts)

        # Back to index page
        return redirect(url_for('index'))

    # GET → Show form with current data
    return render_template('update.html', post=post)


@app.route('/like/<int:post_id>')
def like(post_id):
    """
        Function loads a list of dictionaries of all posts via help-function load_posts,
        search for the given post_id and increases the likes counter by one.
        After that it gives the new data to the help-function save_posts to update the JSON file.
        Finally, it returns to the updated index page.
    """
    
    posts = load_posts()

    for post in posts:
        if post["id"] == post_id:
            # Falls likes noch nicht existiert
            if "likes" not in post:
                post["likes"] = 0

            post["likes"] += 1
            break

    save_posts(posts)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)