install python 3
intall and configure vscode

set up virtual environment(windows)
py -3 - m venv <name-venv>
myvenv\Scripts\activate.bat
pip install fastapi[all] 
pip freeze

to start our server
uvicorn main:app 
uvicorn main:app --reload  (auto rerun on changes in files)

==
While building an API, the "path" is the main way to separate "concerns" and "resources".
decoraters : actual path operation converter 

==why do you need schema
its a pain to all the values from body
the client send whatever data they want 
the data isn't getting validated
we ultimately want to force the client to send data in a schema that we except



==parameters stores in body but we can not store all without schema validation

== body 


== pydantic to map the schema validation from the resource. not dependent on fastapi



== curd operation

any application need curd(create, read, update, delete)

standard : plurals 

create = > post method => /posts     => @app.post("/posts")
read   = > get method =>  /posts/:id => @app.post("/posts/{id}")
read   = > get method =>  /posts    => @app.post("/posts")
update => put/patch   => /posts/:id  => @app.post("/posts/{id}")
delete => delete      => /posts/:id  => @app.post("/posts/{id}")


= ideally every dynamic api calls will store some data or extract some data from the data base 


