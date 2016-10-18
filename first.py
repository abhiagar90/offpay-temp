from flask import Flask, jsonify
import os
from peewee import *

app = Flask(__name__)

def getDB():
    import os
    import psycopg2
    import urlparse

    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])

    pdb = PostgresqlDatabase(url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    return pdb

pdb = getDB()

@app.route("/")
def hello():
    ret = {"result":"helloworld new"}
    return jsonify(ret)

# @app.route('/setup')
# def oneTime():
#     import os
#     import psycopg2
#     import urlparse
#
#     urlparse.uses_netloc.append("postgres")
#     url = urlparse.urlparse(os.environ["DATABASE_URL"])
#
#     conn = psycopg2.connect(
#     database=url.path[1:],
#     user=url.username,
#     password=url.password,
#     host=url.hostname,
#     port=url.port
#     )
#
#     cur = conn.cursor()
#     cur.execute('SELECT * from version()')
#     ver = cur.fetchone()
#     return ver

@app.before_request
def before():
    print 'WWWWWWWWWW BEFORE REQUEST'

def getConnection():
    import os
    import psycopg2
    import urlparse

    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])

    conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
    )
    return conn


@app.route('/db/')
def connectToDB():
    conn = getConnection()
    cur = conn.cursor()
    cur.execute('SELECT version()')
    ver = cur.fetchone()
    return ver

####### MODELS ####################

class BaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = pdb

class User(BaseModel):
    username = CharField()
    uuid = CharField(unique=True)
    email = CharField()

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=1337)
