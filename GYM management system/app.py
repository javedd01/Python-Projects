from email import message
from logging import root
from select import select
from unicodedata import name
from datetime import date

from flask import Flask,render_template,request,redirect,url_for

import pymysql
db_connection = None
tb_cursor = None

app = Flask(__name__)

# function to connect to database
def connectToDb():
    global db_connection, tb_cursor
    db_connection=pymysql.connect(host="localhost",user="root", passwd="",database="gym",port=3306)
    if(db_connection):
        print("done!!!")
        tb_cursor=db_connection.cursor()
    else:
        print("not done")

# function to disconnect from database
def disconnectDb():
    db_connection.close()
    tb_cursor.close()

# function to get data from database
def getAllCustomersData():
    connectToDb()
    selectQuery= "select * from customer;"
    tb_cursor.execute(selectQuery)
    allData = tb_cursor.fetchall()
    disconnectDb()
    print(allData)
    return allData

def insertIntoTable(name,subscription,training_type,fees,joining_date):
    connectToDb()
    inserQuery = "INSERT INTO customer(name,subscription,training_type,fees,joining_date) VALUES(%s, %s, %s, %s,%s);"
    tb_cursor.execute(inserQuery,(name,subscription,training_type,fees,joining_date))
    db_connection.commit()
    disconnectDb()
    return True
#----------------------------------------------------------------START

# funtion for update-delete from database
def getCustomerBasedOnID(id):
    connectToDb()
    selectQuery = "SELECT * FROM customer WHERE ID=%s;"
    tb_cursor.execute(selectQuery,(id,))
    oneData = tb_cursor.fetchone()
    disconnectDb()
    return oneData
def updateCustomerIntoTable(name,subscription,training_type,fees,joining_date,id):
    connectToDb()
    updateQuery = "UPDATE customer SET name=%s,subscription=%s,training_type=%s,fees=%s,joining_date=%s WHERE ID=%s;"
    tb_cursor.execute(updateQuery,(name,subscription,training_type,fees,joining_date,id))
    db_connection.commit()
    disconnectDb()
    return True
def deletecustomerFromTable(id):
    connectToDb()
    deleteQuery = "DELETE FROM customer WHERE ID=%s;"
    tb_cursor.execute(deleteQuery,(id,))
    db_connection.commit()
    disconnectDb()
    return True












#-----------------------------------------------------------------END
@app.route("/")
def  index():
    allCustomers = getAllCustomersData()
    return render_template("index.html",data = allCustomers)

@app.route("/add",methods=["GET","POST"])
def addCustomer():
    if request.method == "POST":
        data = request.form
        isiInserted = insertIntoTable(data['txtName'],data['txtSubscription'],data['txtTraining_type'],data['txtFees'],data['txtJoining_date'])
        if(isiInserted):
            msg= "Customer Data Inserted"
        else:
            msg="Not Inserted"
        return render_template("add.html",message=msg)
    return render_template("add.html")

#-------------------------------------------------------------ROUTE START
@app.route("/update/",methods=["GET","POST"])
def updateCustomer():
    id = request.args.get("ID",type=int,default=1)
    idData = getCustomerBasedOnID(id)
    if request.method == "POST":
        data = request.form
        isUpdated = updateCustomerIntoTable(data['txtName'],data['txtSubscription'],data['txtTraining_type'],data['txtFees'],data['txtJoining_date'],id)
        if(isUpdated):
            
            message = "Updattion sucess"
        else:
            message = "Updattion Error"
        return render_template("update.html",message = message)
    return render_template("update.html",data=idData)

#-----------------------------------------delete query



@app.route("/delete/")
def deletecustomer():
    id = request.args.get("ID",type=int,default=1)
    deletecustomerFromTable(id)
    return redirect(url_for("index"))











if __name__=='__main__':
    app.run(debug=True)