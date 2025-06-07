import os
from flask import Blueprint, flash, redirect, render_template, request, url_for
from models.db import db
from models.fermentation import FermentationProcess

fermentation = Blueprint('fermentation', __name__, url_prefix='/fermentation')

@fermentation.route('/')
def get_fermentations():
    fermentation_list = FermentationProcess.query.all()
    return render_template('fermentation/fermentations.html', fermentations=fermentation_list)

@fermentation.route('/new', methods=['POST'])
def add_fermentation():
    productName = request.form['productName']
    startDate = request.form['startDate']
    temperature = request.form['temperature']
    pH = request.form.get('pH', None)
    acidity = request.form.get('acidity', None)
    status = bool(request.form.get('status', True))

    new_fermentation = FermentationProcess(
        productName=productName,
        startDate=startDate,
        temperature=temperature,
        pH=pH,
        acidity=acidity,
        status=status
    )

    db.session.add(new_fermentation)
    db.session.commit()

    flash('Proceso de fermentación agregado exitosamente!', 'success')
    return redirect(url_for('fermentation.get_fermentations'))

@fermentation.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit_fermentation(id):
    fermentation_process = FermentationProcess.query.get_or_404(id)

    if request.method == 'POST':
        fermentation_process.productName = request.form['productName']
        fermentation_process.startDate = request.form['startDate']
        fermentation_process.temperature = request.form['temperature']
        fermentation_process.pH = request.form.get('pH', None)
        fermentation_process.acidity = request.form.get('acidity', None)
        fermentation_process.status = request.form.get('status') == '1'

        db.session.commit()
        flash('Proceso de fermentación actualizado exitosamente!', 'success')
        return redirect(url_for('fermentation.get_fermentations'))

    return render_template('fermentation/edit_fermentation.html', fermentation=fermentation_process)

@fermentation.route('/delete/<string:id>', methods=['POST'])
def delete_fermentation(id):
    fermentation_process = FermentationProcess.query.get_or_404(id)

    db.session.delete(fermentation_process)
    db.session.commit()
    flash('Proceso de fermentación eliminado exitosamente!', 'success')
    return redirect(url_for('fermentation.get_fermentations'))