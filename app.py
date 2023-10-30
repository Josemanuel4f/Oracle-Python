import os
import sys
import cx_Oracle
from flask import Flask, render_template, request

def init_session(connection, requestedTag_ignored):
    cursor = connection.cursor()
    cursor.execute("""
        ALTER SESSION SET
          TIME_ZONE = 'UTC'
          NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI'""")

# start_pool(): starts the connection pool
def start_pool():
    pool_min = 4
    pool_max = 4
    pool_inc = 0
    pool_gmd = cx_Oracle.SPOOL_ATTRVAL_WAIT

    print("Connecting to", "192.168.122.153:1539/XE")

    pool = cx_Oracle.SessionPool(user="josema",
                                 password="josema",
                                 dsn="192.168.122.153:1539/XE",
                                 min=pool_min,
                                 max=pool_max,
                                 increment=pool_inc,
                                 threaded=True,
                                 getmode=pool_gmd,
                                 sessionCallback=init_session)

    return pool

app = Flask(__name__)

@app.route('/')
def index():
 return render_template("index.html")

# Show the username for a given id
@app.route('/login', methods=['POST'])
def login():
    user=request.form.get("usuario")
    passwd=request.form.get("contraseña")
    connection = pool.acquire()
    cursor = connection.cursor()
    cursor.execute("select nombre from equipos")
    equipos = cursor.fetchall()
    nombres=[]
    for equipo in equipos:
        nombres.append(equipo[0])
    return render_template("login.html",nombres=nombres)
    

################################################################################
#
# Initialization is done once at startup time
#
if __name__ == '__main__':

    # Start a pool of connections
    pool = start_pool()


    # Start a webserver
app.run("0.0.0.0",5000,debug=True)
