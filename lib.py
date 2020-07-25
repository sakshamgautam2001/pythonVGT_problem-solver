import pymysql

def dbcur():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='userdata', autocommit=True)
    cur = conn.cursor()
    return cur

def check_photo(email):
    cur=dbcur()
    sql="select * from photodata where email='"+email+"'"
    cur.execute(sql)
    n=cur.rowcount
    pdt='no'
    if n==1:
        pdt=cur.fetchone()
    return pdt


def ans_data(qid):
    cur=dbcur()
    sql="select * from solution_photo where qid="+qid+""
    cur.execute(sql)
    n=cur.rowcount
    data='no'
    if n>0:
        data=cur.fetchall()
    return data


def myq_data(email):
    cur=dbcur()
    sql="select * from solutions where qby='"+email+"'"
    cur.execute(sql)
    n=cur.rowcount
    data='no'
    if n>0:
        data=cur.fetchall()
    return data


