from program import app
from flask import render_template, redirect, url_for, flash
from program.models import User, Event, Comment
from program.forms import RegisterForm, LoginForm, AddEventForm, AddCommentForm
from program import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home_page.html')

@app.route('/events_list', methods=['GET', 'POST'])
def events_list():
    events = Event.query.order_by(Event.date_start).all()
    return render_template('events_list.html', events=events)

@app.route('/event_page/<int:event_id>', methods=['GET', 'POST'])
def event_page(event_id):
    event = Event.query.get_or_404(event_id)
    comments = Comment.query.filter_by(event_id=event_id).order_by(Comment.date_posted).all()
    form = AddCommentForm()
    if form.validate_on_submit():
        new_comment = Comment(content=form.comment.data, event_id=event_id, author_id=current_user.id)
        db.session.add(new_comment)
        db.session.commit()
        flash('Your comment has been added!', category='success')
        return redirect(url_for('event_page', event_id=event_id))

    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating your comment: {err_msg}', category='danger')

    return render_template('event_page.html', event=event, comments=comments, form=form)

@app.route('/add_event', methods=['GET', 'POST'])
@login_required
def add_event():
    form = AddEventForm()
    if form.validate_on_submit():
        new_event = Event(event_name=form.event_name.data,
                        description=form.description.data,
                        date_start=form.date_start.data,
                        date_end=form.date_end.data,
                        google_link=form.google_link.data,
                        photo_link=form.photo_link.data,
                        owner = current_user.id)
        db.session.add(new_event)
        db.session.commit()
        flash(f"Event {new_event.event_name} created successfully!", category='success')
        return redirect(url_for('events_list'))

    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating an event: {err_msg}', category='danger')

    return render_template('add_event.html', form=form)




@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))









