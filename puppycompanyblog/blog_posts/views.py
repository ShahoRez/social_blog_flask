from flask import render_template, url_for, redirect, flash , request , Blueprint
from puppycompanyblog import db
from puppycompanyblog.blog_posts.forms import BlogPostsForm
from puppycompanyblog.models import BlogPosts,User
from flask_login import login_required, current_user

blog_posts = Blueprint('blog_posts', __name__)


#Create a new blog post
@blog_posts.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    
    form = BlogPostsForm()
    
    if form.validate_on_submit():
        blog_post = BlogPosts(title= form.title.data,
                             content= form.content.data,
                             author_id= current_user.id)
        db.session.add(blog_post)
        db.session.commit()
        flash('Blog post created')
        return redirect(url_for('core.index'))
    
    return render_template('create_post.html', form=form)
    



#View all blog posts

@blog_posts.route('/<int:blog_post_id>')
def blog_post_view(blog_post_id):
    blogpost  = BlogPosts.query.get_or_404(blog_post_id)
    return render_template('blog_post.html' , blogpost=blogpost)




#Update blog posts
@blog_posts.route('/<int:blog_post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(blog_post_id):
    blogpost = BlogPosts.query.get_or_404(blog_post_id)

    if blogpost.author_id != current_user.id :
        abort(403)
        
    form = BlogPostsForm()
    
    if form.validate_on_submit():
        blogpost.title = form.title.data
        blogpost.content = form.content.data
        db.session.commit()
        flash('Blog post updated')
        return redirect(url_for('blogposts.blog_post_view', blog_post_id=blog_post_id))
    elif request.method == 'GET':
        form.title.data = blogpost.title
        form.content.data = blogpost.content
        
    return render_template('create_post.html' , title='Update Post' , form=form)



#Delete blog post

@blog_posts.route('/<int:blog_post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(blog_post_id):
    blogpost = BlogPosts.query.get_or_404(blog_post_id)
    if blogpost.author_id != current_user.id :
        abort(403)
    
    db.session.delete(blogpost)
    db.session.commit()
    flash('Blog post deleted')
    return redirect(url_for('core.index'))