from flask import  render_template , redirect, request , flash , url_for , Blueprint
from flask_login import login_required , current_user , login_user , logout_user
from puppycompanyblog import db
from puppycompanyblog.users.forms import LoginForm, RegistrationForm , UpdateUserForm
from puppycompanyblog.users.picture_handler import add_profile_pic
from puppycompanyblog.models import User , BlogPosts
 
users = Blueprint('users',__name__)

#register
@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User( email= form.email.data,
                    username= form.username.data,
                    password= form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in','success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

#login
@users.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if  user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('You are Logged in successfully')
            
            next = request.args.get('next')
            
            if next == None or not next[0] == '/' :
                next = url_for('core.index')
            
            return redirect(next)
    return render_template('login.html' , form=form)


#logout
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))

#account
@users.route('/account',  methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUserForm()
    
    if form.validate_on_submit():
        if form.picture.data :
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            print(pic)
            current_user.profile_image = pic
         
        current_user.username = form.username.data   
        current_user.email = form.email.data
        current_user.password = form.password.data
        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('users.account'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        
        
    profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', form = form , profile_pic = profile_pic)    


@users.route('/<username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPosts.query.filter_by(author=user).order_by(BlogPosts.date_posted.desc()).pagination(page=page, per_page=5)
    return render_template('user_blog_posts.html' , blog_posts= blog_posts , user=user)