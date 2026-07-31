from flask import Flask, render_template
import json


app = Flask(__name__)


def load_posts():
    with open("blog_data.json", "r", encoding="utf-8") as file:
        return json.load(file)

@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)