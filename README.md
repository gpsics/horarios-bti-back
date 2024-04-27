# SISTEMA WEB BACK-END PARA GERENCIAR HORÁRIOS

## Descrição

O Gerenciador de Horários é uma API desenvolvida em Django com o propósito de facilitar o processo de gerenciamento dos horários para a coordenação do curso de Bacharelado em Tecnologia da Informação (BTI) do Campus Pau dos Ferros (CMPF) da Universidade Federal Rural do Semiárido (UFERSA) antes de cadastrá-los no Sistema Integrado de Gestão de Atividades Acadêmicas (SIGAA). A aplicação visa substituir o método tradicional e ultrapassado de gerenciamento manual de horários, que frequentemente resulta em conflitos acadêmicos e dificuldades para os coordenadores.

## Características e funcionalidades

- Permite o gerenciamento das entidades *Professor*, *Componentes Curriculares* e *Turmas* (CRUD);
- Permite a listagem de turmas filtrada por *Professor*, *Componente Curricular* e por número de semestre do componente; 
- Permite a listagem de turmas com conflitos de horários;
- Possue um sistema de autenticação e autorização, o JWT;
- Possue validação de todos os campos das entidades;

## Pré-requisitos

A fim de garantir que o software seja executado de forma consistente, recomenda-se que a instalação e execução da aplicação seja feita utilizando:
 - `Python 3.11.0`;
 - `Virtualenv 20.23` ou uma versão mais recente.

## Instalação

Para instalar e executar o Gerenciador de Horários localmente, siga e execute os seguintes passos:

- **Passo 1** - Clone este repositório para o seu ambiente local.

- **Passo 2** -  Navegue até o diretório do projeto.
- **Passo 3** -  Crie e ative uma  `virtualenv`
	- Linux:
		~~~
		sudo apt install python3-venv
		python3 -m venv venv
		. venv/bin/activate
		~~~
	- Windows:
		~~~
		python -m venv venv
		.\\venv\Scripts\activate
		~~~
	
- **Passo 4** - Instale as dependências
	~~~
	pip install -r requirements-dev.txt
	~~~	

- **Passo 5** - Na pasta `dotenv_files`, crie uma cópia do arquivo `.env-example` e o renomeei `.env`
	- Execute no terminal 
		~~~
		python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" 	
		~~~
	- Modifique a `SECRET_KEY` do arquivo pela gerada pelo comando 
		~~~
		SECRET_KEY='CHANGE-ME
		~~~
- **Passo 6** - Crie e aplique as modificações no banco de dados
	~~~
	python3 manage.py makemigrations
	python3 manage.py migrate
	~~~
- **Passo 7** - Crie um super usuário
	~~~
	python3 manage.py createsuperuser
	~~~
- **Passo 8** - Rode o servidor
	~~~
	python3 manage.py runserver
	~~~
- **Passo 9** - Por fim, acesse [localhost:8000/admin](http://localhost:8000/admin) e faça login.

## Principais endpoints

ENDPOINTS DE GERENCIAMENTO - 
- Endpoint destinado para realizar as solicitações acerca das `Turmas` (GET POST, PUT, PATCH e DELETE).
	- http://localhost:8000/api/turmas/

- Endpoint destinado para realizar as solicitações acerca dos `Professores` (GET, POST, PUT, PATCH e DELETE).
	- http://localhost:8000/api/professores/

- Endpoint destinado para realizar as solicitações acerca dos `Componentes Curriculares` (GET, POST, PUT, PATCH e DELETE).
	- http://localhost:8000/api/componentes/

ENDPOINTS DE VISUALIZAÇÃO - 

- Endpoint destinado para recuperar os horários das turmas com base em um `Número do Semestre`.
	- [localhost:8000/api/horarios/semestre/`<num_semestre>`/](http://localhost:8000/api/horarios/professores/num_semestre/) 

- Endpoint destinado para recuperar os horários das turmas com base no identificador do `Professor`.
	- [localhost:8000/api/horarios/professores/`<id_prof>`/](http://localhost:8000/api/horarios/professores/id_prof/) 

- Endpoint destinado para recuperar os horários das turmas com base no `Código do Componente Curricular`.
	- [localhost:8000/api/horarios/componentes/`<codigo>`/](http://localhost:8000/api/horarios/componentes/codigo/) 

- Endpoint destinado para recuperar os `Conflitos` de horários presente nas turmas cadastradas.
	- [localhost:8000/api/horarios/conflitos/](http://localhost:8000/api/horarios/conflitos) 


Para mais informações acesso [localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/) ou consulte a nossa documentação.


## Tecnologias e bibliotecas

Para o desenvolvimento desse sistema foi utilizado:
- Python - v3.11.0
- Django - v4.2.3
- Django Rest Framework - v3.14.0
- Simple JWT (JSON Web Token) - 5.3.0
- SQLite e PostgreSQL

## Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo `LICENSE` para obter mais detalhes.


## Contato

Para mais informações sobre o projeto, entre com [gpsics@ufersa.edu.br](mailto:gpsics@ufersa.edu.br).

GPSiCS
