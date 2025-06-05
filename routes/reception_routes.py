from flask import Blueprint, request, jsonify
from models.reception import Reception
from models.db import db
from datetime import datetime

reception_bp= Blueprint('reception_bp', __name__)

@reception_bp.route('reception_bp', methods=['POST'])

def create_reception():
    data = request.get_json()

    new_reception = Reception(
        variety=data['variety'],
        weight=data['weight'],
        acidity=data['acidity'],
        pH=data['pH'],
        date=datetime.strptime(data.get('date'), "%Y-%m-%d") if data.get('date') else datetime.utcnow() 
    )

    db.session.add(new_reception)
    db.session.commit()

    return jsonify({
        "id": new_reception.id,
        "variety": new_reception.variety,
        "weight": new_reception.weight,
        "acidity": new_reception.acidity,
        "pH": new_reception.pH,
        "date": new_reception.date.strftime("%Y-%m-%d"),
        "maturity": new_reception.calculate_maturity()

    }), 201

@reception_bp.route('/receptions', methods=['GET'])
def get_receptions():
    reception = Reception.query.all()
    return jsonify([
        {
            "id": r.id,
            "variety": r.variety,
            "weight": r.weight,
            "acidity": r.acidity,
            "pH": r.pH,
            "date": r.date.strftime("%Y-%m_%d"),
            "maturity": r.calculate_maturity()
        } for r in reception
    ])

#obtengo una recepcion por ID
@reception_bp.route('/reception/<string:reception_id', methods=['GET'])
def get_reception(reception_id):
    reception = Reception.query.get_or_404(reception_id)
    data = request.get_json()

    reception.variety = data.get('variety', reception.variety)
    reception.weight = data.get('weight', reception.weight)
    