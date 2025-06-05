import os
from flask import Blueprint, flash, redirect, render_template, request, url_for
from models.db import db
from models.storage import StorageProcess

storage = Blueprint('storage', __name__, url_prefix='/storage')

@storage.route('/')
def get_storage():
    storage_list = StorageProcess.query.all()
    return render_template('storage/storage.html', storage_items=storage_list)

@storage.route('/new', methods=['POST'])
def add_storage():
    location = request.form['location']
    capacity = request.form['capacity']
    conditions = request.form.get('conditions', None)
    status = bool(request.form.get('status', True))

    new_storage = StorageProcess(
        productName=productName,
        location=location,
        capacity=capacity,
        conditions=conditions,
        status=status
    )

    db.session.add(new_storage)
    db.session.commit()

    flash('Almacenamiento agregado exitosamente!', 'success')
    return redirect(url_for('storage.get_storage'))

@storage.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit_storage(id):
    storage_item = StorageProcess.query.get_or_404(id)

    if request.method == 'POST':
        storage_item.productName = request.form['productName']
        storage_item.location = request.form['location']
        storage_item.capacity = request.form['capacity']
        storage_item.conditions = request.form.get('conditions', None)
        storage_item.status = request.form.get('status') == '1'

        db.session.commit()
        flash('Almacenamiento actualizado exitosamente!', 'success')
        return redirect(url_for('storage.get_storage'))

    return render_template('storage/edit_storage.html', storage_item=storage_item)

@storage.route('/delete/<string:id>', methods=['POST'])
def delete_storage(id):
    storage_item = StorageProcess.query.get_or_404(id)

    db.session.delete(storage_item)
    db.session.commit()
    flash('Almacenamiento eliminado exitosamente!', 'success')
    return redirect(url_for('storage.get_storage'))