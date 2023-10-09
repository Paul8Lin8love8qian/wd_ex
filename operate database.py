import pymysql

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="13888332103Zsl!", 
    database="runoob"
)

cursor = connection.cursor()

query = "select * from runoob_tbl"

cursor.execute(query)

result = cursor.fetchall() 
"""
返回如下
((1, '学习 PHP', '菜鸟教程', datetime.date(2023, 9, 17)), 
 (2, '学习 MySQL', 'RUNOOB>COM', datetime.date(2023, 9, 17)), 
 (4, '学习 python', '菜鸟教程', datetime.date(2023, 9, 17)))
"""

print(result)

cursor.close()
connection.close()