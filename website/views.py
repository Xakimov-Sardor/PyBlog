from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, db, User

views = Blueprint('views', __name__)



# @views.route('/home')
@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user, posts=Post)

@views.route('/create', methods=['POST', 'GET'])
def create_post():

    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')



        if len(title) < 25:
            flash('Title should be at least 25 characters long', category='error')
        elif len(text) < 25:
            flash('Text, should be at least 100 characters long', category='error')
        else:
            new_post = Post(text=text, author=current_user.id, title=title)
            db.session.add(new_post)
            db.session.commit()


            flash('Post created', category='successful')

            return redirect(url_for('views.home')) #then change this

    return render_template('create_post.html', user=current_user)


@views.route('/delete/<id>')
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash('This post not exist', category='error')
    elif post.author != current_user.id:
        flash('You dont have permission for this post', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted', category='successful')
    
    return redirect(url_for('views.home'))

@views.route('/posts/<username>')
@login_required
def user_posts(username):
    
    target_user = User.query.filter_by(username=username).first()

    if not target_user:
        flash('This useraname is not exist', category='error')
        return redirect(url_for('views.home'))
    else:
        posts = target_user.posts
        return render_template('profile.html', username=username, user_posts=posts, user=current_user)