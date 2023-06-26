import mysql.connector


class SQL:
    def __init__(self):
        self.cnx = self.connectSQL()
        self.cursor = self.cnx.cursor()

    def connectSQL(self):
        cnx = mysql.connector.connect(
            host="localhost",
            user="your_username",
            password="your_password",
            database="your_database"
        )

        return cnx

    def insertSQL(self, cnx, cursor):
        cursor = cnx.cursor()

        # 执行插入语句
        insert_query = "INSERT INTO table_name (column1, column2, ...) VALUES (%s, %s, ...)"
        values = ("value1", "value2", ...)
        cursor.execute(insert_query, values)

        # 提交更改
        cnx.commit()

    def selectSQL(self, cnx, cursor):
        cursor = cnx.cursor()
        select_query = "SELECT * FROM table_name"
        cursor.execute(select_query)

        # 获取所有结果
        results = cursor.fetchall()

        # 遍历结果
        for row in results:
            # 处理每一行数据
            column1 = row[0]
            column2 = row[1]
            # ...

    def updataSQL(self, cnx, cursor):
        cursor = cnx.cursor()
        # 执行更新语句
        update_query = "UPDATE table_name SET column1 = %s WHERE condition"
        new_value = "new_value"
        cursor.execute(update_query, (new_value,))

        # 提交更改
        cnx.commit()

    def deleteSQL(self, cnx, cursor):
        cursor = cnx.cursor()
        # 执行删除语句
        delete_query = "DELETE FROM table_name WHERE condition"
        cursor.execute(delete_query)

        # 提交更改
        cnx.commit()

    def closeSQL(self, cursor, cnx):
        cursor.close()
        cnx.close()
