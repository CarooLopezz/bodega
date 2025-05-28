# conecta la interfaz a través de rutas que conectan la base de datos
import os
from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename #seguridad a la imagen
from models.db import db
from models.wines import Wines

products = Blueprint('wines', __name__, url_prefix='/wines')

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@products.route('/')
def get_products():
    products_list = Wines.query.all()
    return render_template('wines/wines.html', products=products_list)


@products.route('/new', methods=['POST'])
def add_product():
    productName = request.form['productName']
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

    new_product = Wines(
        productName=productName,
        origen=origen,
        image=filename

    )

    db.session.add(new_product)
    db.session.commit()

    flash('Producto agregado exitosamente!', 'success')
    return redirect(url_for('wines.get_products'))

#métodos get y post
@products.route('/edit/<string:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Wines.query.get_or_404(id)

    if request.method == 'POST':
        product.productName = request.form['productName']
        product.origen = request.form['origen']

        # Manejar imagen
        image_file = request.files.get('image')
        if image_file and image_file.filename != '':
            if allowed_file(image_file.filename):
                # Borrar imagen vieja
                if product.image:
                    old_imagen_path = os.path.join(UPLOAD_FOLDER, product.imagen)
                    if os.path.exists(old_imagen_path):
                        os.remove(old_imagen_path)
                # Guardar nueva imagen
                image_filename = secure_filename(image_file.filename)
                image_path = os.path.join(UPLOAD_FOLDER, image_filename)
                image_file.save(image_path)
                product.image = image_filename
            else:
                flash(
                    'Formato de imagen no permitido. Solo png, jpg, jpeg, gif.', 'danger')
                return redirect(request.referrer)

        db.session.commit()
        flash('Producto actualizado exitosamente!', 'success')
        return redirect(url_for('wines.get_products'))

    return render_template('wines/edit_products.html', product=product)


@products.route('/delete/<string:id>', methods=['POST'])
def delete_product(id):
    product = Wines.query.get_or_404(id)

    # Borrar imagen si existe
    if product.image:
        image_path = os.path.join(UPLOAD_FOLDER, product.image)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(product)
    db.session.commit()
    flash('Producto eliminado exitosamente!', 'success')
    return redirect(url_for('wines.get_products'))