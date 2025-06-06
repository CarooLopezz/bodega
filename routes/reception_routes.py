# routes/reception_routes.py
import os
from flask import Blueprint, flash, redirect, render_template, request, url_for
from models.db import db
from models.reception import Reception
from datetime import datetime

receptions = Blueprint('receptions', __name__, url_prefix='/receptions')

# Rutas para la gestión de Recepciones

@receptions.route('/')
def get_receptions():
    """Muestra todas las recepciones y el formulario para agregar una nueva."""
    receptions_list = Reception.query.all()
    return render_template('receptions/receptions.html', receptions=receptions_list)

@receptions.route('/new', methods=['POST']) # Cambiado a solo 'POST'
def add_reception():
    """Agrega una nueva recepción (solo acepta POST desde el formulario incluido)."""
    # Obtener datos del formulario
    variety = request.form['variety']
    start_reception_str = request.form['start_reception']
    end_reception_str = request.form['end_reception']
    weight = request.form['weight']
    acidity = request.form['acidity']
    ph = request.form['ph']

    # Convertir strings de fecha a objetos datetime
    start_reception = None
    if start_reception_str:
        try:
            start_reception = datetime.strptime(start_reception_str, "%Y-%m-%d")
        except ValueError:
            flash('Formato de fecha de inicio inválido. Use AAAA-MM-DD.', 'danger')
            return redirect(request.referrer) # Regresa a la página anterior (receptions.html)

    end_reception = None
    if end_reception_str:
        try:
            end_reception = datetime.strptime(end_reception_str, "%Y-%m-%d")
        except ValueError:
            flash('Formato de fecha de fin inválido. Use AAAA-MM-DD.', 'danger')
            return redirect(request.referrer) # Regresa a la página anterior (receptions.html)

    # Convertir a float, manejando posibles errores (aunque `required` en HTML ayuda)
    try:
        weight_float = float(weight)
        acidity_float = float(acidity)
        ph_float = float(ph)
    except ValueError:
        flash('Peso, acidez y pH deben ser números válidos.', 'danger')
        return redirect(request.referrer)

    # Crear nueva instancia de Reception
    new_reception = Reception(
        variety=variety,
        start_reception=start_reception,
        end_reception=end_reception,
        weight=weight_float,
        acidity=acidity_float,
        ph=ph_float
    )

    db.session.add(new_reception)
    db.session.commit()

    flash('Recepción agregada exitosamente!', 'success')
    return redirect(url_for('receptions.get_receptions')) # Redirige a la página principal de recepciones

@receptions.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit_reception(id):
    """Edita una recepción existente."""
    reception = Reception.query.get_or_404(id)

    if request.method == 'POST':
        # Obtener datos del formulario
        reception.variety = request.form['variety']
        start_reception_str = request.form['start_reception']
        end_reception_str = request.form['end_reception']
        
        # Convertir a float, manejando posibles errores
        try:
            reception.weight = float(request.form['weight'])
            reception.acidity = float(request.form['acidity'])
            reception.ph = float(request.form['ph'])
        except ValueError:
            flash('Peso, acidez y pH deben ser números válidos.', 'danger')
            return redirect(request.referrer)

        # Convertir strings de fecha a objetos datetime
        if start_reception_str:
            try:
                reception.start_reception = datetime.strptime(start_reception_str, "%Y-%m-%d")
            except ValueError:
                flash('Formato de fecha de inicio inválido. Use AAAA-MM-DD.', 'danger')
                return redirect(request.referrer)
        else:
            reception.start_reception = None # Si el campo está vacío, establecer a None

        if end_reception_str:
            try:
                reception.end_reception = datetime.strptime(end_reception_str, "%Y-%m-%d")
            except ValueError:
                flash('Formato de fecha de fin inválido. Use AAAA-MM-DD.', 'danger')
                return redirect(request.referrer)
        else:
            reception.end_reception = None # Si el campo está vacío, establecer a None

        db.session.commit()
        flash('Recepción actualizada exitosamente!', 'success')
        return redirect(url_for('receptions.get_receptions'))
    
    return render_template('receptions/edit_reception.html', reception=reception)

@receptions.route('/delete/<string:id>', methods=['POST'])
def delete_reception(id):
    """Elimina una recepción."""
    reception = Reception.query.get_or_404(id)

    db.session.delete(reception)
    db.session.commit()
    flash('Recepción eliminada exitosamente!', 'success')
    return redirect(url_for('receptions.get_receptions'))