import os

from flask import Flask
from flask import request

def create_app(test_config=None):     
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    from . import db
    db.init_app(app)

    def query_db(query, args=(), one=False):
        cur = db.get_db().execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    @app.route("/name", methods=['GET', 'POST'])
    def get_name():
        if request.method == "POST":
            return "<p>jexhsu from POST</p>"
        else:
            return "<p>jexhsu from GET</p>" 

    @app.route("/fans")
    def get_fans():
        return "<p>zero</p>"

    ## 用户资料endpoint
    # sqlite 增删改查
    # 1. 获取数据库连接
    # 2. 获取一个数据库的游标 cursor
    # 3. 写sql
    # 4. 执行sql
    # 5. 处理从数据库中读取的数据
    # 6. 将数据返回给调用者
    @app.route("/userProfile", methods=['GET', "POST", "PUT", "DELETE"])
    def get_profile():
        ## R: read 
        if request.method == "GET":
            uid = request.args.get("uid", 1)
            connection = db.get_db()
            query = "SELECT * FROM userProflie WHERE id={}".format(uid)
            cursor = connection.execute(query)
            result = cursor.fetchone()
            if result is not None:
                return dict(username=result["username"], fans=result["fans"])
            else:
                return dict(message="user doesn't exist")
        ## C: create 
        elif request.method == "POST":
            name = request.json.get("name")
            fans = request.json.get("fans")
            connection = db.get_db()
            query = "INSERT INTO userProflie (username, fans) values('{}', {})".format(name, fans)
            try: 
                cursor = connection.execute(query)
                connection.commit()
                print(cursor.lastrowid)
                return dict(success=True)
            except:
                return dict(success=False, message="user exist")
        ## U: update
        elif request.method == "PUT":
            uid = request.args.get("uid", 1)
            name = request.json.get("name")
            fans = request.json.get("fans")
            connection = db.get_db()
            query = "UPDATE userProflie SET username='{}', fans={} WHERE id={}".format(name, fans, uid)
            cursor = connection.execute(query)
            connection.commit()
            if cursor.rowcount > 0:
                return dict(success=True)
            else:
                return dict(success=False, message="user doesn't exist")
        ## D: delete  
        elif request.method == "DELETE":
            uid = request.args.get("uid", 1) 
            connection = db.get_db()
            query = "DELETE FROM userProflie WHERE id = {}".format(uid)            
            cursor = connection.execute(query)
            connection.commit()
        if cursor.rowcount > 0:
            return dict(success=True)
        else:
            return dict(success=False, message="user doesn't exist")
            
    return app