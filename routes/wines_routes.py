# conecta la interfaz a través de rutas que conectan la base de datos
import os
from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename #seguridad a la imagen
from models.db import db
from models.wines import Wines

wines = Blueprint('wines', __name__)

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@wines.route('/')
def get_wine():
    wines_list = Wines.query.all()
    return render_template('wines/wines.html', wines=wines_list)


@wines.route('/new', methods=['GET','POST'])
def add_wine():
    if request.method == 'POST':
        name = request.form['name']
        origen = request.form['origen']
        image_file = request.files.get('image')
        filename = None
      
    
        if image_file and image_file.filename != '':
            if allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                image_path = os.path.join(UPLOAD_FOLDER, filename)
                image_file.save(image_path)
            else:
                flash('Formato de imagen no permitido. Solo png, jpg, jpeg, gif.', 'danger')
                return redirect(request.referrer)

        new_wine = Wines(
            name=name,
            origen=origen,
            image=filename

        )

        db.session.add(new_wine)
        db.session.commit()

        flash('Producto agregado exitosamente!', 'success')
        return redirect(url_for('wines.get_wine'))
    
    return render_template('wines/new_wine.html')

#métodos get y post
@wines.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit_wine(id):
    wines = Wines.query.get_or_404(id)

    if request.method == 'POST':
        wines.productName = request.form['name']
        wines.origen = request.form['origen']

        # Manejar imagen
        image_file = request.files.get('image')
        if image_file and image_file.filename != '':
            if allowed_file(image_file.filename):
                # Borrar imagen vieja
                if wines.image:
                    old_image_path = os.path.join(UPLOAD_FOLDER, wines.image)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                # Guardar nueva imagen
                image_filename = secure_filename(image_file.filename)
                image_path = os.path.join(UPLOAD_FOLDER, image_filename)
                image_file.save(image_path)
                wines.image = image_filename
            else:
                flash(
                    'Formato de imagen no permitido. Solo png, jpg, jpeg, gif.', 'danger')
                return redirect(request.referrer)

        db.session.commit()
        flash('Producto actualizado exitosamente!', 'success')
        return redirect(url_for('wines.get_wines'))

    return render_template('wines/edit_wines.html', wines=wines)


@wines.route('/delete/<string:id>', methods=[ 'POST'])
def delete_wine(id):
    wine = Wines.query.get_or_404(id)

    # Borrar imagen si existe
    if wine.image:
        image_path = os.path.join(UPLOAD_FOLDER, wine.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(wine)
    db.session.commit()
    flash('Producto eliminado exitosamente!', 'success')
    return redirect(url_for('wines.get_wine'))