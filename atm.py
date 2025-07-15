import csv,time,os,mysql.connector as mc
def register(u,p):
    f=open("atm.csv","r",newline="")
    r=csv.reader(f)
    for i in r:
        if i[0]==u:
            choice=input("USER EXISTS. DO YOU WANT TO LOGIN? [Y/N]").upper()
            print()
            if choice=="Y":
                f.close()
                login(u,p)
            elif choice=="N":
                print("TRY USING DIFFERENT USER NAME")
                f.close()
                main()
            else:
                print("PLEASE TRY AGAIN WITH VALID INPUT")
                print()
                main()
    f.close()
    add_sql(u,p)
    f=open("atm.csv","a",newline="")
    w=csv.writer(f)
    w.writerow([u,p,0])
    f.close()
    menu(u,p)
def login(u,p):
    f=open("atm.csv","r",newline="")
    r=csv.reader(f)
    for i in r:
        if i[0]==u:
            if i[1]==p:
                print("LOGIN SUCCESSFULL")
                f.close()
                menu(u,p)
            else:
                print("ACCESS DENIED")
                f.close()
                main()
    f.close()
    choice=input("USER DON'T EXIST. DO YOU WANT TO REGISTER? [Y/N]").upper()
    print()
    if choice=="Y":
        register(u,p)
    elif choice=="N":
        print("TRY USING DIFFERENT USER NAME")
        main()
    else:
        print("PLEASE TRY AGAIN WITH VALID INPUT")
        print()
        main()
def balance(u,p):
    f=open("atm.csv","r",newline="")
    r=csv.reader(f)
    for i in r:
        if i[0]==u:
            b=float(i[2])
            print("YOUR BANK BALANCE IS : RS.",b)
    f.close()
    return b
def deposit(u,p):
    try:
        b=balance(u,p)
        m=float(input("HOW MUCH MONEY DO YOU WANT TO DEPOSIT?"))
        f1=open("atm.csv","r",newline="")
        f2=open("temp.csv","w",newline="")
        r=csv.reader(f1)
        w=csv.writer(f2)
        for i in r:
            if i[0]==u:
                w.writerow([u,p,b+m])
            else:
                w.writerow(i)
        f1.close()
        f2.close()
        os.remove("atm.csv")
        os.rename("temp.csv","atm.csv")
        update_sql(u,p)
        log(u,b,"DEPOSIT",m,b+m)
        menu(u,p)
    except:
        print()
        print("PLEASE TRY AGAIN WITH VALID INPUT")
        print()
        deposit(u,p)
def withdraw(u,p):
    try:
        b=balance(u,p)
        m=float(input("HOW MUCH MONEY DO YOU WANT TO WITHDRAW?"))
        while m>b:
            print("INSUFFICIENT BALANCE")
            m=float(input("HOW MUCH MONEY DO YOU WANT TO WITHDRAW?"))
        f1=open("atm.csv","r",newline="")
        f2=open("temp.csv","w",newline="")
        r=csv.reader(f1)
        w=csv.writer(f2)
        for i in r:
            if i[0]==u:
                w.writerow([u,p,b-m])
            else:
                w.writerow(i)
        f1.close()
        f2.close()
        os.remove("atm.csv")
        os.rename("temp.csv","atm.csv")
        update_sql(u,p)
        log(u,b,"WITHDRAW",m,b-m)
        menu(u,p)
    except:
        print()
        print("PLEASE TRY AGAIN WITH VALID INPUT")
        print()
        withdraw(u,p)
def change(u,p):
    try:
        f1=open("atm.csv","r",newline="")
        f2=open("temp.csv","w",newline="")
        r=csv.reader(f1)
        w=csv.writer(f2)
        for i in r:
            if i[0]==u:
                np=int(input("ENTER YOUR NEW PIN : "))
                w.writerow([u,np,i[2]])
            else:
                w.writerow(i)
        f1.close()
        f2.close()
        os.remove("atm.csv")
        os.rename("temp.csv","atm.csv")
        update_sql(u,np)
        menu(u,p)
    except():
        f1.close()
        f2.close()
        print()
        print("PLEASE TRY AGAIN WITH VALID INPUT")
        print()
        change(u,p)
def add_sql(u,p):
    con=mc.connect(host="localhost",user="root",passwd="tiger",database="atm")
    cur=con.cursor()
    cur.execute("insert into atm values('{0}','{1}',{2});".format(u,p,0))
    con.commit()
    con.close()
def update_sql(u,p):
    con=mc.connect(host="localhost",user="root",passwd="tiger",database="atm")
    cur=con.cursor()
    cur.execute("update atm set pin='{0}',balance={1} where user='{2}';".format(p,balance(u,p),u))
    con.commit()
    con.close()
def log(u,b,act,amt,net_amt):
    f=open("log.txt","a")
    f.write(time.asctime()+":"+u+","+str(b)+","+act+","+str(amt)+","+str(net_amt)+"\n")
    f.close()
def menu(u,p):
    try:
        print()
        print("1. CHECK BALANCE\n2. DEPOSIT MONEY\n3. WITHDRAW MONEY\n4. CHANGE PIN\n5. QUIT")
        choice=int(input("ENTER YOUR CHOICE : "))
        print()
        if choice==1:
            balance(u,p)
            menu(u,p)
        elif choice==2:
            deposit(u,p)
        elif choice==3:
            withdraw(u,p)
        elif choice==4:
            change(u,p)
        elif choice==5:
            quit()
        else:
            raise Exception
    except:
        print()
        print("PLEASE TRY AGAIN WITH VALID INPUT")
        print()
        menu(u,p)
def main():
    try:
        print()
        print("WELCOME TO ABCD BANK ATM")
        print("1. REGISTER\n2. LOGIN\n3. QUIT")
        choice=int(input("ENTER YOUR CHOICE : "))
        print()
        if choice==1:
            user=input("ENTER USER NAME : ").upper()
            pin=input("ENTER USER PIN : ")
            register(user,pin)
        elif choice==2:
            user=input("ENTER USER NAME : ").upper()
            pin=input("ENTER USER PIN : ")
            login(user,pin)
        elif choice==3:
            quit()
        else:
            raise Exception
    except:
        print()
        print("PLEASE TRY AGAIN WITH VALID INPUT")
        print()
        main()
main()