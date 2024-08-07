from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
from kanboard_gsa_api.services import KanboardHookService
import os

load_dotenv()

bp = Blueprint('kanboard_hook', __name__)

@bp.route('/fechar-chamados', methods=['POST'])
def fechar_chamados():
    token = request.args.get('token')
    
    if token != os.getenv('KANBOARD_HOOK_TOKEN'):
        return jsonify({'status': 'error'}), 403
    
    kanboard_hook_service = KanboardHookService()
    
    data = request.json
    response, status_code = kanboard_hook_service.processa_evento_kanboard(data)
    
    return jsonify(response), status_code
