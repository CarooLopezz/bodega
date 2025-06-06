from flask import Blueprint, flash, redirect, render_template, request, url_for
from models.db import db
from models.user import User 

users = Blueprint('users', __name__, url_prefix='/users')


@users.route('/')
def get_users():
    users_list = User.query.all()
    return render_template('users/users.html', users=users_list)


@users.route('/new', methods=['POST'])
def add_users():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    role = request.form.get('role', 'user')

    new_user = User(
        username=username,
        email=email,
        password=password,
        role=role
    )

    db.session.add(new_user)
    db.session.commit()

    flash('Usuario agregado exitosamente!', 'success')
    return redirect(url_for('users.get_users'))


@users.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get_or_404(id)

    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.password = request.form['password']
        user.role = request.form.get('role', 'user')

        db.session.commit()
        flash('Usuario actualizado exitosamente!', 'success')
        return redirect(url_for('users.get_users'))

    return render_template('users/edit_users.html', user=user)


@users.route('/delete/<string:id>', methods=['POST'])
def delete_user(id):
    user = User.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()
    flash('Usuario eliminado exitosamente!', 'success')
    return redirect(url_for('users.get_users'))
