import csv,mysql.connector as sqltor
def setup():
    f1=open("atm.sql","r")
    sql_setup(None,None,0)
    f2=open("log.txt","r")
    r=f2.readline()
    f2.close()
    f3=open("atm.csv","w",newline="")
    w=csv.writer(f3)
    w.writerow(["user","pin","balance"])
    f3.close()
    usr,paswd=r.split(",")
    paswd=paswd.rstrip("\n")
    con=sqltor.connect(host="localhost",user=usr,passwd=paswd)
    cur=con.cursor()
    for i in f1:
        cur.execute(i[:-1] if i.endswith("\n") else i)
    con.commit()
    con.close()
    return usr,paswd
def sql_setup(usr,paswd,sql_status):
    while sql_status==0:
        usr=input("ENTER MYSQL USER NAME : ")
        paswd=input("ENTER MYSQL USER PASSWORD : ")
        try:
            con=sqltor.connect(host="localhost",user=usr,passwd=paswd)
            if con.is_connected():
                con.close()
                f=open("log.txt","w")
                f.write(usr+","+paswd+"\n")
                f.close()
                print("SQL CONNECTION SUCCESSFUL")
                print()
                sql_status=1
        except:
            print("SQL CONNECTION FAILED. PLEASE TRY AGAIN")
            print()
usr,paswd=setup()