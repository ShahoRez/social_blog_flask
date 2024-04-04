from flask import render_template,redirect,Blueprint , request
from puppycompanyblog.models import BlogPosts

core = Blueprint('core',__name__)

@core.route('/')
def index():
    page = request.args.get('page',1 , type=int)
    posts = BlogPosts.query.order_by(BlogPosts.date_posted.desc()).paginate(page=page , per_page=2)
    return render_template('index.html' , posts=posts)

@core.route('/about')
def about():
    return render_template('about.html')