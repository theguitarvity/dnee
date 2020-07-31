# DNEE - Dynamic News Extraction Engine
 Respositório reservado para o projeto de pesquisa, referente a extração de notícias em tempo real.

## Instruções de clonagem e execução do projeto

#### Pré-requisitos
* Python 3.x devidamente instalado e configurado;
* Ambiente Virtual(venv) configurado;

#### Passos de instalação e configuração


* Abrir o terminal
* Criar venv
```
    python3 -m venv myvenv
```
* Entrar no venv
``` 
    source myvenv/bin/activate
```
* Instalar o django
```
  pip install django
```
* Clonar repositório 
```
    git clone https://git.facom.ufms.br/ic-victorlopes/fakehunter.git
```
* Entrar no diretório
```
  cd fakehunter
```



* Instalar dependências do projeto
```
  pip install -r requeriments.txt
```
* Criar superuser
```
    python manage.py createsuperuser
```

* Executar o projeto

```
 python manage.py runserver
```
Após o passo anterior, abrir localhost:8000 no navegador.



* Logar no DNEE

Com o seu super usuario criado, basta somente logar com suas credenciais.

![alt text](http://imgur.com/QlRYBkg.png)


## Instruções de uso

### Utilização do DNEE

* Calibrar o motor de extração

Após a execução do servidor pelo comando runserver, deve-se calibrar o MED(Motor de extração dinâmica).
```
    Recarregar o site no navegador 3x, para o motor ser calibrado.

```
* Painel de controle do DNEE, com os agentes em execução
![alt text](http://imgur.com/PD5Okjz.png)

* Pagina individual de um agente qualquer

![alt text](http://imgur.com/qU7dR2Y.png)

* Relatório gerado pelo botão "Gerar Relatório"

![alt text](http://imgur.com/jwDSbXG.png)

* Relatorio de todos os agentes em extração

![alt text](http://imgur.com/SRgCR2U.png)

* Adicionar um agente manualmente, caso queira extrair notícias de algum site especifico

```
    Clicar em "Adicionar Agente Manualmente"
```
![alt text](http://imgur.com/f9mRKUb.png)


### Conclusão

Portanto, somente é necessário deixar o DNEE trabalhar, que o mesmo irá extrair, em tempo real, todas as noticias do momento.








