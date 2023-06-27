import mysql.connector
import json

class SQL:
    def __init__(self):
        self.cnx = self.connectSQL()
        self.cursor = self.cnx.cursor()

    def __connectSQL__(self):

        cnx = mysql.connector.connect(
            host="localhost",
            user="username",
            password="password",
            database="database"
        )

        return cnx

    def insertSQL(self, cnx, cursor):

        # # 执行插入语句
        # insert_query = "INSERT INTO table_name (column1, column2, ...) VALUES (%s, %s, ...)"
        # values = ("value1", "value2", ...)
        # cursor.execute(insert_query, values)
        #
        # # 提交更改
        # cnx.commit()

        # 列表转换为字符串
        data_list = [1, 2, 3, 4]
        data_str = json.dumps(data_list)

        # 执行插入语句
        insert_query = "INSERT INTO table_name (column_name) VALUES (%s)"
        values = (data_str,)
        cursor.execute(insert_query, values)

        # 提交更改
        cnx.commit()

    def selectSQL(self, cursor):

        # select_query = "SELECT * FROM table_name"
        # cursor.execute(select_query)
        #
        # # 获取所有结果
        # results = cursor.fetchall()
        #
        # # 遍历结果
        # for row in results:
        #     # 处理每一行数据
        #     column1 = row[0]
        #     column2 = row[1]
        #     # ...

        # 执行查询语句
        select_query = "SELECT column_name FROM table_name"
        cursor.execute(select_query)

        # 获取结果
        result = cursor.fetchone()
        data_str = result[0]

        # 字符串转换为列表
        data_list = json.loads(data_str)

        # 遍历列表
        for item in data_list:
            print(item)

    def updataSQL(self, cnx, cursor):

        # 执行更新语句
        # update_query = "UPDATE table_name SET column1 = %s WHERE condition"
        # new_value = "new_value"
        # cursor.execute(update_query, (new_value,))
        #
        # # 提交更改
        # cnx.commit()

        # 新的列表数据
        new_data_list = [5, 6, 7]

        # 列表转换为字符串
        new_data_str = json.dumps(new_data_list)

        # 执行更新语句
        update_query = "UPDATE table_name SET column_name = %s WHERE condition"
        values = (new_data_str,)
        cursor.execute(update_query, values)

        # 提交更改
        cnx.commit()

    def deleteSQL(self, cnx, cursor):

        # 执行删除语句
        delete_query = "DELETE FROM table_name WHERE condition"
        cursor.execute(delete_query)

        # 提交更改
        cnx.commit()

    def closeSQL(self, cursor, cnx):

        # 关闭游标对象和数据库连接
        cursor.close()
        cnx.close()
