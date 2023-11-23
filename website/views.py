from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, db, User, Comment, Like

views = Blueprint('views', __name__)



# @views.route('/home')
@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user, posts=Post, like=Like)

@views.route('/create', methods=['POST', 'GET'])
def create_post():

    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')



        if len(title) < 25:
            flash('Title should be at least 25 characters long',category='error')
        elif len(text) < 25:
            flash('Text, should be at least 100 characters long',category='error')
        else:
            new_post = Post(text=text, author_id=current_user.id, title=title)
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
    elif post.author_id != current_user.id:
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
        if target_user.username == current_user.username:
            username = 'My'
        return render_template('user_posts.html', username=username, user_posts=posts, user=current_user)

@views.route('/post/<id>', methods=['POST', 'GET'])
@login_required
def post_detail_view(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash('This post not exist', category='error')
        return redirect(url_for('views.home'))
    else:
        if request.method == 'POST':
            text = request.form.get('text')

            if len(text) < 5:
                flash('Comment must be', category='error')

            else:
                
                new_comment = Comment(text=text, post_id=post.id, author=current_user.username)
                db.session.add(new_comment)
                db.session.commit()

                flash('Comment created', category='successful')
                return redirect(url_for('views.post_detail_view', id=id))
        return render_template('post_detail.html', post=post, user=current_user)
    
# @views.route('/deleteit/<id>')
# def ok(id):
#     user = User.query.filter_by(id=id).delete()

#     db.session.commit()

#     return redirect(url_for('views.home'))


@views.route('/delete-coment/<id>')
def delete_coment(id):
    comment = Comment.query.filter_by(id=id).first()

    if not comment:
        flash('Comment not exist', category='error')
        return redirect(url_for('views.home'))
    else:
        db.session.delete(comment)
        db.session.commit()

        flash('Comment deleted', category='successful')

        return redirect(url_for('views.post_detail_view', id=comment.post_id))
@views.route('/like/<post_id>')
def like_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if not post:
        flash('Post does not exist', category='error')
    else:
        like = Like.query.filter_by(author_id=current_user.id, post_id=post.id).first()
        if not like:
            new_like = Like(author_id=current_user.id, post_id=post.id)
            db.session.add(new_like)
            db.session.commit()

        else:
            db.session.delete(like)
            db.session.commit()

        
            

    return redirect(url_for('views.home'))