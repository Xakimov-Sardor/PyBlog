from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Post, db, User

views = Blueprint('views', __name__)


# @views.route('/home')
@views.route('/')
@login_required
def home():
    return render_template('home.html', user_for_home=current_user)

@views.route('/create', methods=['POST', 'GET'])
def create_post():

    if request.method == 'POST':
        text = request.form.get('text')

        if len(text) < 50:
            flash('Text should be at least 50 characters long', category='error')

        else:
            new_post = Post(text=text, author=current_user.id)
            db.session.add(new_post)
            db.session.commit()


            flash('Post created', category='successful')

    return render_template('create_post.html', user=current_user)


@views.route('/post/<int:user_id>')
def detail_post(user_id):

    return render_template('posts_div.html', post=Post.query.filter_by(id=user_id).first(), User=User)