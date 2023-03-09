from flask import Flask, render_template,request,redirect,url_for
from mysql.connector import connect  

con=connect(host='localhost',
            port=3306,
            database='banking',
            user='root')

myapp = Flask(__name__)
@myapp.route('/')
def home():
    return render_template('index.html')

@myapp.route('/viewAllCustomers')
def viewCustomers():
    cur=con.cursor()
    cur.execute("SELECT * FROM customer")
    res=cur.fetchall()
    return render_template("customers.html",data=res)

@myapp.route('/viewProfile/<string:name>',methods=['POST'])
def viewProfile(name):
    cur=con.cursor()
    cur.execute("SELECT * FROM customer where name=%s",(name,))
    res=cur.fetchall()
    return render_template("profile.html",data=res)
@myapp.route('/transfer/<string:name>')
def viewTransfer(name):
    cur=con.cursor()
    cur.execute("SELECT * FROM customer where name!=%s",(name,))
    res=cur.fetchall()
    return render_template("transferTo.html",data=res,user=name)
@myapp.route('/transferProfile/<string:name>',methods=['POST'])
def transferProfile(name):
    cur=con.cursor()
    cur.execute("SELECT * FROM customer where name=%s",(name,))
    res=cur.fetchall()
    return render_template("profile.html",data=res)

@myapp.route('/transferAccount/<string:user>',methods=['POST'])
def transferAccount(user):
    if request.method=="POST":
        name=request.form['name']
        amount=request.form['amount']
        amount=int(amount)
        cur=con.cursor()
        cur.execute("SELECT `Current Balance` FROM customer where name=%s",(user,))
        res=cur.fetchall()
        if amount>int(res[0][0]):
            return "Insufficient balance"
        else:
            cur.execute("UPDATE customer SET `Current Balance` = `Current Balance` + %s where name=%s",(amount,name))
            cur.execute("UPDATE customer SET `Current Balance` = `Current Balance` - %s where name=%s",(amount,user))
            cur.execute("INSERT INTO transaction(Sender, Receiver, Amount) VALUES (%s,%s,%s)",(user,name,amount))
            con.commit()
            return redirect(url_for('viewCustomers'))

@myapp.route('/transactions')
def transactions():
    cur=con.cursor()
    cur.execute("SELECT * FROM transaction")
    res=cur.fetchall()
    return render_template("history.html",data=res)
if __name__=="__main__":
    myapp.run(debug=True)