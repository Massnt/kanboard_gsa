import re
import pprint
import os
import kanboard
from datetime import datetime
from dotenv import load_dotenv
from kanboard_gsa_api.services import GsaApiService


class KanboardHookService:
    def __init__(self):
        load_dotenv()
        
        self._kb = kanboard.Client(os.getenv('KANBOARD_API_URL'), 'jsonrpc', os.getenv('KANBOARD_API_TOKEN'))
    
    def processa_evento_kanboard(self, data):
        changes = data.get('event_data').get('changes')
        task = data.get('event_data').get('task')
        
        if data.get('event_name') == 'task.update':
            if changes.get('color_id') == 'green' and task.get('column_id') == int(os.getenv('KANBOARD_COL_EM_PRODUCAO')):
                return self.handle_task_update(task, 'RC')
            
            if changes.get('category_id') == os.getenv('KANBOARD_REPROVADO_ID'):
                self._kb.execute('moveTaskPosition', project_id=1, task_id=task.get('id'), column_id=5, position=1, swimlane_id=1)
                return self.handle_task_update(task, 'RP')
            
        if data.get('event_name') == 'task.move.column' and changes.get('dst_column_id') == os.getenv('KANBOARD_COL_REPROVADO'):
            self._kb.execute('updateTask', id=task.get('id'), category_id='4')
            return self.handle_task_update(task, 'RP')

        return {'status': 'error'}, 405
    
    def handle_task_update(self, task, acao):
        gsa_api_service = GsaApiService()
        
        try:
            cliente_nome, atendente_nome = self.extrair_nomes(task)
        except (AttributeError, TypeError):
            return {'status': 'error', 'message': 'Titulo de tarefa inválido'}, 400
        
        resultado_cliente, resultado_atendente = self.get_cliente_e_atendente(gsa_api_service, cliente_nome, atendente_nome)
        
        if resultado_cliente.get('status') == 'error':
            return resultado_cliente, 500
        
        if resultado_atendente.get('status') == 'error':
            return resultado_atendente, 500
        
        dados = self.construir_dados(task, resultado_cliente, resultado_atendente, acao)
        
        pprint.pp(dados)
        
        resultado = gsa_api_service.finalizar_chamado(dados)
        
        if resultado.get('status') == 'success':
            return resultado.get('data'), 200
        
        return {'status': 'error'}, 500
    
    def extrair_nomes(self, task):
        cliente_nome = re.search(r'\[(.*?)\]', task.get('title')).group(1)
        atendente_nome = task.get('creator_username')
        return cliente_nome, atendente_nome
    
    def get_cliente_e_atendente(self, gsa_api_service, cliente_nome, atendente_nome):
        resultado_cliente = gsa_api_service.get_cliente(cliente_nome)
        resultado_atendente = gsa_api_service.get_atendente(atendente_nome)
        return resultado_cliente, resultado_atendente
    
    def construir_dados(self, task, resultado_cliente, resultado_atendente, acao):
        cliente_id = resultado_cliente.get('data').get('cliente_id')
        atendente_id = resultado_atendente.get('data').get('atendente_id')
        
        data_criacao = datetime.fromtimestamp(task.get('date_creation')).strftime('%d-%m-%Y').replace('-', '/')
        
        dados = {
            'cliente_id'            : cliente_id,
            'objeto_id'             : '6',
            'assunto'               : task.get('title').split(']')[1].replace('-', '').strip(),
            'texto'                 : task.get('description'),
            'prioridade_id'         : '1',
            'atendente_id'          : atendente_id,
            'descricao_da_conclusao': 'OK' if acao == 'RC' else 'REPROVADO',
            'status_id'             : 4,
            'data_criacao'          : data_criacao,
            'data_da_conclusao'     : datetime.today().strftime('%d-%m-%Y').replace('-', '/')
        }
        return dados
