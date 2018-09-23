import MySQLdb

def connection():
    conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="#33FalleN666",
                           db="FitBro")
    c = conn.cursor()
    return c, conn