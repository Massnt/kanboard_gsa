from dotenv import load_dotenv
import requests
import os

class GsaApiService:
    def __init__(self):
        load_dotenv()
        
        self._url = os.getenv('GSA_API_URL')
        self._token = os.getenv('GSA_API_TOKEN')
        
        if not self._url or not self._token:
            raise ValueError("GSA_API_URL e GSA_API_TOKEN devem estar configuradas no .env")
        
        self._retorno_base = {
            'status' : '',
            'message': '',
            'data'   : '',
            'errors' : '',
        }
    
    def _make_request(self, endpoint, search):
        url = f"{self._url}{endpoint}"
        data = {
            'search' : search,
            'token'  : self._token
        }
        
        try:
            response = requests.get(url, json=data)
            response.raise_for_status()
        except requests.RequestException as e:
            return {
                'status' : 'error',
                'message': str(e),
                'data'   : '',
                'errors' : response.json() if response else str(e),
            }
        
        return response.json()
    
    def get_cliente(self, nome):
        resultado = self._make_request('cliente', nome)
        
        if resultado.get('data'):
            self._cliente = resultado.get('data')[0]
            retorno = self._retorno_base.copy()
            retorno.update({
                'status': 'success',
                'data': {'cliente_id': self._cliente.get('id')}
            })
            return retorno
        else:
            retorno = self._retorno_base.copy()
            retorno.update({
                'status': 'error',
                'message': 'Cliente não encontrado',
            })
            return retorno
    
    def get_atendente(self, nome):
        resultado = self._make_request('atendente', nome)
        
        if resultado.get('data'):
            self._atendente = resultado.get('data')[0]
            retorno = self._retorno_base.copy()
            retorno.update({
                'status': 'success',
                'data': {'atendente_id': self._atendente.get('id')}
            })
            return retorno
        else:
            retorno = self._retorno_base.copy()
            retorno.update({
                'status': 'error',
                'message': 'Atendente não encontrado',
            })
            return retorno
        
    def finalizar_chamado(self, dados_kanboard):
        url = f'{self._url}chamados'
        
        dados = dados_kanboard.copy()
        dados['token'] = self._token
        print(dados)
        
        try:
            response = requests.post(url, json=dados)
            response.raise_for_status()
        except requests.RequestException as e:
            return {
                'status' : 'error',
                'message': str(e),
                'data'   : '',
                'errors' : response.json() if response else str(e),
            }
            
        retorno = self._retorno_base.copy()    
           
        if response.json():
            retorno.update({"status" : "success", "data" : response.json()})
            
            return retorno
        
        retorno.update({"status" : "error"})
        
        return retorno
