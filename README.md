## challenge_ml
### Para executar
#
`python3 challenge.py`
#
Foi realizado a identação do arquivo `dblist.json`.</br>
O script começa lendo o arquivo `dblist.json` que contem as informações sobre as bases de dados(para teste local, pode-se alterar o campo `e-mail` desse arquivo, dessa forma você conseguirá testar o envio de e-mail para você mesmo).</br> O arquivo JSON é processado para extrair a lista de bases de dados, `dn_name`, `classification` e o `owner`.

Em seguida, o script lê o arquivo CSV que contém informações sobre os usuários e seus gerentes. O arquivo CSV é processado para mapear o `user_id` do usuário ao email do gerente correspondente. Essas informações são armazenadas em um dicionário.

O script cria uma conexão com o banco de dados SQLite (ou cria o banco de dados se ele não existir) e define a estrutura da tabela `revdb.db`.

Para cada item na lista de bases de dados obtidos do arquivo `dblist.json`, o script insere as informações relevantes na tabela `revdb.db` do banco de dados SQLite, isso inclui o nome da base de dados `dn_name`, o nome do proprietário `owner` -> `name`, o email do gerente `manager_email` obtido do dicionário mapeado a partir do arquivo CSV e a classificação da base de dados.

Em seguida, o script verifica se a classificação da base de dados é alta (high) (em lower para não ocorrer erros). Se der match, o script envia um email para o gerente correspondente, informando que a base de dados está pendente de revalidação e solicitando sua aprovação. Isso é feito usando a biblioteca smtplib (abaixo todas os links de documentações das libs) para enviar emails através de uma conta do Gmail(especificamente).

Por fim, o script faz o commit das alterações no banco de dados e fecha a conexão.

Resumindo, o script lê os arquivos `dblist.json` e `user_manager.csv`, armazena as informações `dn_name`, `owner_name`, `manager_email`, `classification` em um banco de dados SQLite e envia emails aos gerentes para bases de dados com classificação alta.

#
Obs.: Não se esqueça de alterar/inserir seu e-mail do GMAIL e sua senha de app localizada nas configurações de sua conta google:</b>
> configurações->segurança->senhas de app</br>
#
### Envio de e-mail
1. Revalidação `locations`
![](/imagens/locations.png)</br>
2. Revalidação `orders`
![](/imagens/orders.png)</br>
3. Revalidação `users`
![](/imagens/users.png)</br>
#
### Aviso de envio
![](/imagens/envia_email.png)
#
### Tabela em sqlite3
![](/imagens/tabela_sql.png)</br>
#

## Links úteis | Docs
- [Documentação lib json](https://docs.python.org/3/library/json.html)</br>                    
- [Documentação lib csv](https://docs.python.org/3/library/csv.html)</br>                     
- [Documentação lib smtp](https://docs.python.org/3/library/smtplib.html)</br>
- [Documentação lib ssl](https://docs.python.org/3/library/ssl.html)</br>
- [Documentação lib MIMEText](https://docs.python.org/pt-br/3.7/library/email.mime.html)</br>      