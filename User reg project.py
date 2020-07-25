from flask import Flask,render_template,redirect,request,url_for,session
import pymysql
from lib import *
from werkzeug.utils import secure_filename
import time
import os



app=Flask(__name__)



app.secret_key='super secret key'

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/login',methods=['GET','POST'])
def login():

    if request.method == 'POST':
        email = request.form['T1']
        passwd = request.form['T2']
        cur = dbcur()
        sql = "select * from login where email='" + email + "' and password='" + passwd + "'"
        cur.execute(sql)
        n = cur.rowcount
        if n == 1:
            data = cur.fetchone()
            ut = data[2]
            # make sessions
            session['email'] = email
            session['usertype'] = ut
            if ut == 'admin':
                return redirect(url_for('admin_home'))
            else:
                return redirect(url_for('user_home'))
        else:
                return render_template('Login.html', msg='enter correct email or password')



    else:
        return render_template('Login.html')

@app.route('/home')
def home():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='admin':
            return redirect(url_for('admin_home'))
        else:
            return redirect(url_for('user_home'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/admin_home')
def admin_home():
    if 'usertype' in session:
        ut=session['usertype']
        el=session['email']
        if ut=='admin':
            photo=check_photo(el)
            return render_template('AdminHome.html',el=el,photo=photo)
        else:
            return redirect(url_for('auth_error'))

    else:
        return redirect(url_for('auth_error'))

@app.route('/user_home')
def user_home():
    if 'usertype' in session:
        ut = session['usertype']
        el=session['email']
        if ut == 'user':
            photo = check_photo(el)
            return render_template('UserHome.html',el=el,photo=photo)
        else:
            return redirect(url_for('auth_error'))

    else:
        return redirect(url_for('auth_error'))

@app.route('/auth_error')
def auth_error():
    return render_template('AuthorizationError.html')

@app.route('/logout')
def logout():
    if 'usertype' in session:
        session.pop('usertype',None)
        session.pop('email',None)
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route('/change_password',methods=['GET','POST'])
def change_password():
    if 'usertype' in session:
        ut=session['usertype']
        if request.method == 'POST':
            opass = request.form['T1']
            npass = request.form['T2']
            email = session['email']
            cur = dbcur()
            sql = "update login set password='" + npass + "' where email='" + email + "' and password='" + opass + "'"
            cur.execute(sql)
            n = cur.rowcount
            if n == 1:
                return render_template('ChangePassword.html', msg='password updated')
            else:
                return render_template('ChangePassword.html', msg='enter valid old password')
        else:
            return render_template('ChangePassword.html')





    else:
        return redirect(url_for('auth_error'))







@app.route('/admin_reg',methods=['GET','POST'])
def admin_reg():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='admin':
            if request.method == 'POST':
                name = request.form['T1']
                roll = request.form['T2']
                branch = request.form['T3']
                add = request.form['T4']
                cont = request.form['T5']
                email = request.form['T6']
                passwd = request.form['T7']
                usertype = 'admin'

                conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='userdata',
                                       autocommit=True)
                cur = conn.cursor()
                s1 = "insert into intro values('" + name + "','" + roll + "','" + branch + "','" + add + "','" + cont + "','" + email + "')"
                s2 = "insert into login values('" + email + "','" + passwd + "','" + usertype + "')"

                try:
                    cur.execute(s1)
                    n = cur.rowcount
                    cur.execute(s2)
                    m = cur.rowcount
                    msg = 'Error try again'
                    if m == 1 and n == 1:
                        msg = 'both user and login saved'
                    elif m == 1:
                        msg = 'only login data saved'
                    elif n == 1:
                        msg = 'only user data saved'
                    return render_template('Adminreg.html', mg=msg)

                except pymysql.err.IntegrityError:
                    return render_template('AdminReg.html',mg='Email already exists,try again')


            else:
                return render_template('Adminreg.html')
        else:
            return redirect(url_for('auth_error'))
    else:
        return redirect(url_for('auth_error'))

@app.route('/sign_up')
def sign_up():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='admin':
            return redirect(url_for('admin_reg'))
        else:
            return redirect(url_for('user_reg'))
    else:
        return redirect(url_for('user_reg'))



@app.route('/user_reg',methods=['GET','POST'])
def user_reg():
    if request.method=='POST':
        name = request.form['T1']
        roll = request.form['T2']
        branch = request.form['T3']
        add = request.form['T4']
        cont = request.form['T5']
        email = request.form['T6']
        passwd = request.form['T7']
        usertype = 'user'

        conn=pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='userdata',autocommit=True)
        cur=conn.cursor()
        s1="insert into intro values('"+name+"','"+roll+"','"+branch+"','"+add+"','"+cont+"','"+email+"')"
        s2="insert into login values('"+email+"','"+passwd+"','"+usertype+"')"

        try:
            cur.execute(s1)
            n = cur.rowcount
            cur.execute(s2)
            m = cur.rowcount
            msg = 'Error try again'
            if m == 1 and n == 1:
                msg = 'both user and login saved'
            elif m == 1:
                msg = 'only login data saved'
            elif n == 1:
                msg = 'only user data saved'
            return render_template('reg.html', mg=msg)
        except pymysql.err.IntegrityError:
            return render_template('reg.html',mg='Email already exists')


    else:
        return render_template('reg.html')


@app.route('/show_user')
def show_user():
    if 'usertype' in session:
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='userdata', autocommit=True)
        cur = conn.cursor()
        sql = "select * from intro"
        cur.execute(sql)
        n = cur.rowcount
        if n > 0:
            data = cur.fetchall()
            return render_template('show.html', dt=data)
        else:
            return render_template('show.html', mg='No available data')
    else:
        return redirect(url_for('auth_error'))

@app.route('/edit_user',methods=['GET','POST'])
def edit_user():
    if 'usertype' in session:
        if request.method == 'POST':
            email = request.form['AA']
            conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='userdata', autocommit=True)
            cur = conn.cursor()
            sql = "select * from intro where email='" + email + "'"
            cur.execute(sql)
            n = cur.rowcount
            if n == 1:
                data = cur.fetchone()
                return render_template('edit.html', dt=data)
            else:
                return render_template('edit.html', msg='no data found')
        else:
            return redirect(url_for('show_user'))
    else:
        return redirect(url_for('auth_error'))


@app.route('/update_user',methods=['GET','POST'])
def update_user():
    if 'usertype' in session:
        if request.method == 'POST':

            conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='userdata', autocommit=True)
            cur = conn.cursor()
            name = request.form['T1']
            roll = request.form['T2']
            branch = request.form['T3']
            add = request.form['T4']
            cont = request.form['T5']
            email = request.form['T6']
            sql = "update intro set name='" + name + "',roll_number='" + roll + "',branch='" + branch + "',address='" + add + "',contact='" + cont + "' where email='" + email + "'"

            cur.execute(sql)
            n = cur.rowcount
            if n == 1:
                return render_template('update.html', mg='data updated')
            else:
                return render_template('update.html', mg='no update')
        else:
            return redirect(url_for('show_user'))
    else:
        return redirect(url_for('auth_error'))



@app.route('/ask_question',methods=['GET','POST'])
def ask_question():
    if 'usertype' in session:
        ut=session['usertype']
        el=session['email']
        if ut=='user':
            ph=check_photo(el)
            if ph=='no':
                return redirect(url_for('upload_photo'))
            else:
                if request.method=='POST':
                    qby=session['email']
                    qdate=str(int(time.time()))
                    qsub=request.form['T1']
                    ques=request.form['T2']
                    qtype=request.form['T3']
                    cur=dbcur()
                    sql="insert into qbank(qsubject,question,qdate,qby,qtype) values('"+qsub+"','"+ques+"',"+qdate+",'"+qby+"','"+qtype+"')"
                    cur.execute(sql)
                    n=cur.rowcount
                    if n==1:
                        return render_template('AskQuestion.html',msg='question posted successfully')
                    else:
                        return render_template('AskQuestion.html', msg='Error: Try again')

                else:
                    return render_template('AskQuestion.html')

        else:
            return redirect(url_for('auth_error'))

    else:
        return redirect(url_for('auth_error'))

@app.route('/my_questions')
def my_questions():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='user':
            email = session['email']
            cur = dbcur()
            sql = "select * from qbank where qby='" + email + "'"
            cur.execute(sql)
            n = cur.rowcount



            if n > 0:
                data = cur.fetchall()
                return render_template('MyQuestions.html', dt=data)
            else:
                return render_template('MyQuestions.html', msg='No Question asked')

        else:
            return redirect(url_for('auth_error'))



    else:
        return redirect(url_for('auth_error'))






@app.route('/answer_questions',methods=['GET','POST'])
def answer_questions():
    if 'usertype' in session:
        ut=session['usertype']
        el=session['email']
        if ut=='user':
            ph=check_photo(el)
            if ph=='no':
                return redirect(url_for('upload_photo'))
            else:
                if request.method == 'GET':
                    email = el
                    cur = dbcur()
                    #here we are allowing those questions which have a profile photo, hence it is necessary to have a profile pic.
                    sql = "select * from question_photo where qby<>'" + email + "' "
                    cur.execute(sql)
                    n = cur.rowcount
                    if n > 0:
                        data = cur.fetchall()
                        return render_template('AnswerQuestions.html', dt=data)

                    else:
                        return render_template('AnswerQuestions.html', msg='No Questions Found')

                else:
                    #fetch data

                    qid = request.form['H1']
                    cur = dbcur()
                    sql = "select * from question_photo where qid=" + qid + " "
                    cur.execute(sql)
                    n = cur.rowcount



                    if n == 1:

                        data = cur.fetchone()
                        return render_template('AnswerQuestions.html', a=data)

                    else:
                        return render_template('AnswerQuestions.html', msg='no question found of this type')




        else:
            return redirect(url_for('auth_error'))


    else:
        return redirect(url_for('auth_error'))







@app.route('/upload_solution',methods=['GET','POST'])
def upload_solution():
    if 'usertype' in session:
        ut=session['usertype']
        el=session['email']
        if ut=='user':
            ph=check_photo(el)
            if ph=='no':
                return redirect(url_for('upload_photo'))
            else:
                if request.method=='POST':
                    qid=request.form['B3']
                    sol=request.form['B1']
                    com=request.form['B2']
                    qby=request.form['B4']
                    cur=dbcur()
                    solby=el
                    soldate=str(int(time.time()))
                    sql="insert into solutions(qid,solution,sol_date,sol_by,comments,qby) values("+qid+",'"+sol+"',"+soldate+",'"+solby+"','"+com+"','"+qby+"')"
                    cur.execute(sql)
                    n=cur.rowcount
                    if n==1:
                        return render_template('UploadSolution.html',msg='solution uploaded successfully')
                    else:
                        return render_template('UploadSolution.html', msg='Error:Try again')
                else:
                    return redirect(url_for('answer_questions'))




        else:
            return redirect(url_for('auth_error'))

    else:
        return redirect(url_for('auth_error'))



app.config['UPLOAD_FOLDER']='./static/photos'



@app.route('/upload_photo',methods=['GET','POST'])
def upload_photo():
    if 'usertype' in session:
        el=session['email']
        if request.method=='POST':
            f=request.files['F1']
            if f:
                path=os.path.basename(f.filename)
                f_ext=os.path.splitext(path)[1][1:]
                filenm=str(int(time.time()))+'.'+f_ext
                fname=secure_filename(filenm)
                cur=dbcur()
                sql="insert into photodata values('"+fname+"','"+el+"')"
                sql2="update intro set photo='"+fname+"' where email='"+el+"' "

                try:
                    cur.execute(sql)

                    n=cur.rowcount
                    cur.execute(sql2)
                    m=cur.rowcount
                    if n==1 and m==1:
                        f.save(os.path.join(app.config['UPLOAD_FOLDER'],fname))
                        return render_template('UploadPhoto1.html',msg='success')
                    else:
                        return render_template('UploadPhoto1.html', msg='failure')

                except:
                    return render_template('UploadPhoto1.html', msg='duplicate')






            else:
                return render_template('UploadPhoto.html',msg='No file found')



        else:
            return render_template('UploadPhoto.html')

    else:
        return redirect(url_for('auth_error'))




@app.route('/change_photo',methods=['GET','POST'])
def change_photo():
    if 'usertype' in session:
        el=session['email']
        ut=session['usertype']
        if request.method == 'POST':
            f = request.files['N1']
            if f:
                cur = dbcur()
                photo = check_photo(el)
                try:
                    s1 = "delete from photodata where email='" + el + "'"
                    cur.execute(s1)

                    os.remove("./static/photos/" + photo[0])

                except:
                    pass

                path = os.path.basename(f.filename)
                f_ext = os.path.splitext(path)[1][1:]
                filenm = str(int(time.time())) + '.' + f_ext
                fname = secure_filename(filenm)

                s2 = "insert into photodata values('" + fname + "','" + el + "')"
                s3="update intro set photo='"+fname+"' where email='"+el+"' "

                cur.execute(s2)
                n = cur.rowcount
                cur.execute(s3)
                m=cur.rowcount
                if n == 1 and m==1:
                    f.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
                    return render_template('ChangePhoto.html', msg='success')
                else:
                    return render_template('ChangePhoto.html', msg='failure')





            else:
                return render_template('ChangePhoto.html', msg='no file found')

        else:
            return render_template('ChangePhoto.html')


    else:
        return redirect(url_for('auth_error'))

@app.route('/show_free_questions',methods=['GET','POST'])
def show_free_questions():
    if request.method=='POST':
        cur=dbcur()
        value=request.form['OP']

        if value=='Motivational':
            sql="select * from question_photo where qtype='"+value+"' "

        elif value=='Cooking':
            sql = "select * from question_photo where qtype='" + value + " '"

        elif value=='Academics':
            sql = "select * from question_photo where qtype='" + value + "'"
        elif value=='Select':
            return render_template('ShowFreeQuestions.html',msg='Please select an option')


        cur.execute(sql)
        n=cur.rowcount
        if n>0:
            data=cur.fetchall()
            return render_template('ShowFreeQuestions.html', data=data)
        else:
            return render_template('ShowFreeQuestions.html',msg='No questions of this type')

    else:
        return redirect(url_for('auth_error'))


@app.route('/find_solution',methods=['GET','POST'])
def find_solution():
    if 'usertype' in session:
        ut=session['usertype']
        if ut=='user':
            if request.method=='POST':
                cur=dbcur()
                qid=request.form['H1']
                sql="select * from solution_photo where qid='"+qid+"'"
                cur.execute(sql)
                n=cur.rowcount
                if n>0:
                    dt=cur.fetchall()
                    return render_template('FindSolution.html',dt=dt)
                else:
                    return render_template('FindSolution.html',msg='No solutions found')

            else:
                return redirect(url_for('my_questions'))
        else:
            return redirect(url_for('auth_error'))

    else:
        return redirect(url_for('auth_error'))




@app.route('/delete_photo',methods=['GET','POST'])

def delete_photo():
    if 'usertype' in session:
        ut=session['usertype']
        el=session['email']

        if request.method=='POST':
            cur=dbcur()

            photo=check_photo(el)
            try:
                os.remove("./static/photos/" + photo[0])
                s1 = "delete from photodata where email='" + el + "'"
                cur.execute(s1)
                s2 = "update intro set photo='no' where email='" + el + "'"
                cur.execute(s2)
            except:
                pass


            if ut=='user':
                return redirect(url_for('user_home'))
            else:
                return redirect(url_for('admin_home'))


        else:
            return render_template('DeletePhoto.html')
    else:
        return redirect(url_for('auth_error'))





















if __name__=='__main__':
    app.run(debug=True)