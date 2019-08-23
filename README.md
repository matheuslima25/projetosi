# ProjetoSI

Projeto criado com o intúito de ser utilizado para crumprir para com as exigências da cadeira Projeto de Sistemas de Informação 
do Curso de Bacharelado em Sistemas de Informação da UNIFIP.

1. Create python 3 virtualenv
> virtualenv -p python3 projetosi

2. Activate virtualenv
> cd projetosi
> . bin/activate

3. Clone repository
> git clone <repo>

4. Go to repository
> cd projetosi

5. Install libs
> pip install -r requirements.txt

6. Run migrate, to create a local database
> python manage.py migrate

7. Create a superuser
> python manage.py createsuperuser

8. Run test server
> python manage.py runserver
