from flask import Flask,render_template,redirect,request,jsonify,url_for
def create_app():
    app = Flask(__name__,template_folder='templates',static_folder='static',static_url_path='/static')
    app.secret_key = 'OHsoiiohsadoihoisadhfoi'

    @app.route('/home')
    def home():
        return render_template('home.html')
    

    @app.route('/')
    def login():
        return render_template('login.html')
    
    
    @app.route('/analyse')
    def analyse():
        return render_template('analyse.html')

    @app.route('/history',methods=['GET','POST'])
    def history():
        data = {'title':''}
        error = ''
        res=''
        if request.method == 'POST':    
            # print(111)
            data = dict(request.form)
            res=data['title']
            res = 2 * int(res)



            
        # print(data)
        return render_template('history.html',res=res)#**data

    @app.route('/view')
    def view():
        return render_template('view.html')
    
    return app