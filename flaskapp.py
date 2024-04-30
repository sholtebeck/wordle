import MySQLdb
db = MySQLdb.connect("skipflog.mysql.pythonanywhere-services.com","skipflog","Smh.sql-24","skipflog$default")
cursor = db.cursor()
cursor.execute("INSERT into words (word) value ('test')")
cursor.execute("SELECT * FROM words")

for x in cursor:
    print(x)

cursor.close()
db.close()
        