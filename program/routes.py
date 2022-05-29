from program import app, db, admin, MyModelView
from flask import render_template, redirect, url_for, flash
from program.models import User, Event, Comment
from program.forms import RegisterForm, LoginForm, AddEventForm, AddCommentForm, SetFullName
from flask_login import login_user, logout_user, login_required, current_user


admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Event, db.session))
admin.add_view(MyModelView(Comment, db.session))


@app.route('/')
def index():
    return render_template('home_page.html')

@app.route('/admin')
@login_required
def admin_page():
    pass

@app.route('/home')
def home_page():
    return render_template('home_page.html')


@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile_page(username):
    this_user = User.query.filter_by(username=username).first_or_404()
    my_events = Event.query.filter_by(owner=this_user.id).all()
    formSetName = SetFullName()
    if formSetName.validate_on_submit():
        this_user.fullName = formSetName.full_name.data
        db.session.commit()
        flash(f"Your profile updated successfully!", category='success')
        return redirect(url_for('profile_page', username=current_user.username))

    if formSetName.errors != {}: #If there are not errors from the validations
        for err_msg in formSetName.errors.values():
            flash(f'There was an error with updating your profile: {err_msg}', category='danger')

    return render_template('profile_page.html' , my_events=my_events, this_user=this_user, formSetName=formSetName)


@app.route('/events_list', methods=['GET', 'POST'])
def events_list():
    events = Event.query.order_by(Event.date_start).all()
    return render_template('events_list.html', events=events)

@app.route('/FAQ')
def FAQ():
    return render_template('faq_page.html')

@app.route('/event_page/<int:event_id>', methods=['GET', 'POST'])
def event_page(event_id):
    event = Event.query.get_or_404(event_id)
    comments = Comment.query.filter_by(event_id=event_id).order_by(Comment.date_posted).all()
    form = AddCommentForm()
    if form.validate_on_submit():
        new_comment = Comment(content=form.comment.data, author_of_comment=current_user, event_id=event_id)
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
                        owner_of_event = current_user)
        db.session.add(new_event)
        db.session.commit()
        flash(f"Event {new_event.event_name} created successfully!", category='success')
        return redirect(url_for('events_list'))

    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating an event: {err_msg}', category='danger')
    return render_template('add_event.html', form=form)


@app.route('/update_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = AddEventForm()
    if form.validate_on_submit():
        event.event_name = form.event_name.data
        event.description = form.description.data
        event.date_start = form.date_start.data
        event.date_end = form.date_end.data
        event.google_link = form.google_link.data
        event.photo_link = form.photo_link.data
        db.session.commit()
        flash(f"Event {event.event_name} updated successfully!", category='success')
        return redirect(url_for('events_list'))

    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with updating an event: {err_msg}', category='danger')
    return render_template('update_event.html', form=form, event=event)
    


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
        return redirect(url_for('index'))
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
            return redirect(url_for('index'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("index"))









