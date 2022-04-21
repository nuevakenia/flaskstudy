from ast import Try
from flask import Flask, jsonify, redirect, render_template, request, url_for, flash
from flask_login import LoginManager, login_user,logout_user,login_required
from flask_mysqldb import MySQL
from config import config

from models.ModelUser import ModelUser
from models.entities.User import User
app=Flask(__name__)



conexion = MySQL(app)
login_manager_app=LoginManager(app)
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(conexion,id)
""" @app.before_request
def before_request():
    print("antes de la petición")

@app.after_request
def after_request():
    print("despues de la petición")
 """

@app.route('/')
def index():
    npc =['goblin','orc','witch']
    data={
        "titulo":"Index",
        "bienvenida":"Saludos",
        "enemigos":npc,
        "numero_npc":len(npc)
    }
    return render_template("index.html", data=data)

@app.route('/contacto/<nombre>')
def contacto(nombre):
    data = {
        "titulo":"Contacto",
        "nombre":nombre
    }
    return render_template("contacto.html",data=data)

def query_string():
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    return "Ok"

@app.route('/npcs', methods=['GET'])
def listar_npc():
    data={}
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT id,nombre,nivel FROM npc ORDER BY nombre ASC"
        cursor.execute(sql)
        npc=cursor.fetchall() # convierte la info devuelta de la db en datos para python.
        lista_npc =[]
        data["npc"]=npc
        data['mensaje']='Exito ...'
        for fila in npc:
            npc={'id':fila[0],"nombre":fila[1],"nivel":fila[2]}
            lista_npc.append(npc)
        return jsonify({"npcs":lista_npc,"mensaje":"Listado NPC"})
    except Exception as ex:
        data['mensaje']='Error ...'
    return jsonify(data)
    
@app.route("/npc/<id>",methods=["GET"])
def detalle_npc(id):
    data={}
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT id,nombre,nivel FROM npc WHERE id = '{0}' ORDER BY nombre ASC".format(id)
        cursor.execute(sql)
        datos=cursor.fetchone() # convierte la info devuelta de la db en datos para python.
        if datos != None:
            npc={'id':datos[0],"nombre":datos[1],"nivel":datos[2]}
            #lista_npc.append(npc)
        return jsonify({"npcs":npc,"mensaje":"Listado NPC"})
    except Exception as ex:
        
        data['mensaje']='Error ...'
    return jsonify(data)

@app.route('/crear', methods=["POST"])
def crear_npc():
    print("JSON: ",request.json)
    try:
        cursor = conexion.connection.cursor()
        sql="""INSERT INTO npc(id,nombre,nivel,fuerza,hp)
        VALUES ('{0}','{1}','{2}','{3}','{4}')""".format(request.json['id'],request.json['nombre'],request.json['nivel'],request.json['fuerza'],request.json['hp'])
        cursor.execute(sql)#Ejecuta la query en la conexion.
        conexion.connection.commit()#confirma el POST (commit).
        
        return jsonify({"mensaje":"Exito!"})
    except Exception as ex:
        return jsonify({"mensaje":"Error"})

@app.route('/actualizar/<id>', methods=["PUT"])
def modificar_npc(id):
    print("JSON: ",request.json)
    try:
        cursor = conexion.connection.cursor()
        sql="""UPDATE npc SET nombre='{1}',nivel='{2}',fuerza='{3}',hp='{4}' WHERE id='{0}'
          """.format(id,request.json['nombre'],request.json['nivel'],request.json['fuerza'],request.json['hp'])
        cursor.execute(sql)#Ejecuta la query en la conexion.
        conexion.connection.commit()#confirma el POST (commit).
        
        return jsonify({"mensaje":"Update con Exito!"})
    except Exception as ex:
        return jsonify({"mensaje":"Error"})



@app.route('/auth/login',methods=["GET",'POST'])
def login():
    if request.method == 'POST':
        print(request.form["nombre"])
        print(request.form["password"])
        user = User(0,request.form["nombre"],request.form["password"])
        logged_user =ModelUser.login(conexion,user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                print("LOGEADO CON EXITO")
                return redirect(url_for("index"))
            else:
                print("PASSWORD INVALIDA")
                flash("Password Inválida")
                return render_template('auth/login.html')
        else:
            flash("Usuario no encontrado")
            print("USUARIO INVALIDA")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@app.route('/auth/registrar',methods=["GET",'POST'])
def registrar():
    if request.method == 'POST':
        print(request.form["nombre"])
        print(request.form["password"])
        user = User(0,request.form["nombre"],request.form["password"])
        logged_user =ModelUser.login(conexion,user)
        if logged_user != None:
            if logged_user.password:
                return redirect(url_for("auth/login.html"))
            else:
                flash("Password Inválida")
                return render_template('auth/login.html')
        else:
            flash("Usuario no encontrado")
            return render_template('auth/login.html')
    
    return render_template('auth/login.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

def pagina_no_encontrada(error):
    return "pagina_no_encontrada",404
    #return render_template("404.html"),404
    #return redirect(url_for("index"))

if __name__=='__main__':
    app.config.from_object(config["development"])
    app.add_url_rule("/query_string", view_func=query_string)
    app.register_error_handler(404,pagina_no_encontrada)
    app.run()
