# Main Import
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Import Models
from flask_app.models.user import User
from flask_app.models.show import Show
from flask_app.models.comment import Comment

# Login page
@app.route('/')
def home():
    return render_template('home.html')

# Processing for new accounts
@app.route('/register', methods=['POST'])
def register():

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['register_email'],
        "register_password_1" : request.form['register_password_1'],
        "register_password_2" : request.form['register_password_2']
    }
    if not User.validate_user(data):
        return redirect('/')


    pw_hash = bcrypt.generate_password_hash(request.form['register_password_1'])
    print(pw_hash)

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['register_email'],
        "password" : pw_hash
    }

    user_id = User.save(data)

    session['user_id'] = user_id
    return redirect("/shows")

    
# Processing for logins
@app.route('/login', methods=['POST'])
def login():

    data = { "email" : request.form["login_email"] }
    user_in_db = User.get_user(data)

    if not user_in_db:
        flash("Invalid Email/Password", 'login')
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['login_password']):

        flash("Invalid Email/Password", 'login')
        return redirect('/')

    session['user_id'] = user_in_db.id

    return redirect("/shows")

# Main page of list of shows
@app.route('/shows')
def shows():
    if 'user_id' in session:
        user = User.get_user_by_id(session['user_id'])
        shows = Show.get_all_shows_with_user()
        return render_template('shows.html', user = user, shows = shows)
    return redirect('/')

# Specific show page
@app.route('/shows/<show_id>')
def show_show(show_id):
    show = Show.get_show_by_id(show_id)
    user = User.get_user_by_id(session['user_id'])
    creator = User.get_user_by_id(show[0]['user_id'])
    comments = Comment.get_all_comments_with_user(show_id)
    session['show_id'] = show_id
    return render_template('show_show.html', show = show, user = user,creator = creator, comments = comments)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# Add a new show
@app.route('/shows/new')
def create():
    if 'show_id' in session:
        del session['show_id']
    show={}
    if 'user_id' in session:
        if 'description' in session:
            show = session['description']
            del session['description']
        return render_template('create.html', show = show)
    return redirect('/')

# Processing for adding a new show
@app.route('/shows/new/submit', methods=['POST'])
def create_show():
    data = {
        "title": request.form['title'],
        "network": request.form['network'],
        "release_date": request.form['date'],
        "comments" : request.form['comments'],
    }
    if not Show.validate_show(data):
        return redirect('/shows/new')
    del session['description']
    data = {
        "title": request.form['title'],
        "network": request.form['network'],
        "release_date": request.form['date'],
        "comments" : request.form['comments'],
        "user_id": session['user_id']
    }

    Show.save(data)
    return redirect("/shows")

# Delete show if the logged in user made that show
@app.route('/shows/delete/<show_id>')
def delete_show(show_id):
    shows = Show.get_show_by_id(show_id)
    if shows[0]['user_id'] == session['user_id']:
        Show.delete_show(show_id)
    return redirect('/shows')

# Edit show if logged in user made the show
@app.route('/shows/edit/<show_id>')
def edit(show_id):
    show = Show.get_show_by_id(show_id)[0]
    session['show_id'] = show_id
    if show['user_id'] == session['user_id']:
        if 'description' in session:
            show = session['description']
            del session['description']
        return render_template('edit.html', show = show)
    return redirect('/')

# Processing for editing a show
@app.route('/shows/edit/submit', methods=['POST'])
def edit_show():
    data = {
        "title": request.form['title'],
        "network": request.form['network'],
        "release_date": request.form['date'],
        "comments": request.form['comments'],
    }
    if not Show.validate_show(data):
        return redirect('/shows/edit/{}'.format(session['show_id']))
    del session['description']
    data = {
        "title": request.form['title'],
        "network": request.form['network'],
        "release_date": request.form['date'],
        "comments" : request.form['comments'],
        "id": session['show_id']
    }
    
    Show.update(data)
    return redirect("/shows")

# New comments
@app.route('/shows/new-comment', methods=['POST'])
def new_comment():
    data = {
        'comment' : request.form['comments'],
        'show_id' : session['show_id'],
        'user_id' : session['user_id']
    }
    Comment.save(data)
    return redirect('/shows/{}'.format(session['show_id']))

#delete Comment
@app.route('/shows/comment-delete/<comment_id>')
def delete_comment(comment_id):
    comment = Comment.get_comment_by_id(comment_id)[0]['user_id']
    if comment == session['user_id']:
        Comment.delete(comment_id)
    return redirect('/shows/{}'.format(session['show_id']))