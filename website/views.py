from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('/home/dev/code/github/Projects/PyBlog/website/template/home.html')