# Integração Kanboard GSA

## Requisitos
* Python 3.10.12
* Pipenv

## Instalação
Inicialmente é necessário clonar este repositório:
```
git clone https://github.com/Massnt/kanboard_gsa.git
```
Em seguida, é necessário ter o python 3.10.12 instalado na máquina.
Com o python instalado, basta instalar a lib de ambientes virtuais do python o pienv,
com o seguinte comando:
```
python3 -m pip install pipenv
```
Após a instalação do módulo, dentro da pasta kanboard_gsa do repositório clonado,
basta rodar o seguinte comando:
```
python3 -m pipenv install --system --deploy
```
Neste momento todas dependências necessárias para rodar o projeto estão instaladas.

## Configuração
Na pasta do projeto existe o arquivo .env.example, onde deve ser configurado algumas coisas do sistema.
  * A URL e o Token do GSA;
  * A URL e o Token do webhook do Kanboard;
  * Os ids das colunas de produção e reprovado;
  * O id da categoria **REPROVADO**;
  * URL e Token da API do Kanboard;
  * A porta em que a aplicação irá rodar.
No Kanboard é necessário configurar a url do webhook que vai escutar os eventos, no caso será
está aplicação. Por padrão a aplicação flask roda nos seguintes endereços:
´´´
http://localhost:PORTA_ESCOLHIDA
´´´  
´´´
http://127.0.0.1:PORTA_ESCOLHIDA
´´´  
## Execução
Para executar o projeto é simples, basta rodar o seguinte código dentro da pasta kanboard_gsa:
```
python3 app.py
```
