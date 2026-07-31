from flask import Flask, render_template, request, redirect, url_for
import json


app = Flask(__name__)


def load_posts():
    with open("blog_data.json", "r", encoding="utf-8") as file:
        return json.load(file)
    

def save_posts(posts):
    with open("blog_data.json", "w", encoding="utf-8") as file:
        json.dump(posts, file, indent=4, ensure_ascii=False)
        

@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Takes new data from form
        title = request.form.get('title')
        content = request.form.get('content')
        author = request.form.get('author')

        # Load existing posts from JSON file via load_posts function
        posts = load_posts()

        # First looking for the next ID, then adds the new post to the existing data
        if posts:
            new_id = max(post["id"] for post in posts) + 1
        else:
            new_id = 1
        
        new_post = {
            "id": new_id,
            "title": title,
            "content": content,
            "author": author
        }
        
        posts.append(new_post)

        # Saves new data to JSON file via save_posts function
        save_posts(posts)

        # Back to index page
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    # Load existing posts from JSON file via load_posts function
    posts = load_posts()
    
    # Deletes post with selected ID
    posts = [post for post in posts if post["id"] != post_id]

    # Saves new data to JSON file via save_posts function
    save_posts(posts)

    # Back to index page
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)