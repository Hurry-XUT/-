import mysql.connector
# 数据库连接配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'deng1217',
    'database': 'library_management'
}
def connect_to_db():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"数据库连接失败: {err}")
        return None

# 添加图书
def add_book(title, publisher, author, publication_date, loan_period=30, stock=10):
    conn = connect_to_db()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO Books (Title, Publisher, Author, PublicationDate, LoanPeriod, Stock)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (title, publisher, author, publication_date, loan_period, stock))
        conn.commit()
        print(f"成功添加图书: {title}")
    except mysql.connector.Error as err:
        print(f"添加图书失败: {err}")
    finally:
        cursor.close()
        conn.close()
# 删除图书
def delete_book(book_id):
    conn = connect_to_db()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        query = "DELETE FROM Books WHERE BookID = %s"
        cursor.execute(query, (book_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"成功删除图书 ID: {book_id}")
        else:
            print(f"未找到图书 ID: {book_id}")
    except mysql.connector.Error as err:
        print(f"删除图书失败: {err}")
    finally:
        cursor.close()
        conn.close()
# 更新图书信息
def update_book(book_id, **kwargs):
    conn = connect_to_db()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        fields = ", ".join(f"{key} = %s" for key in kwargs.keys())
        query = f"UPDATE Books SET {fields} WHERE BookID = %s"
        values = list(kwargs.values()) + [book_id]
        cursor.execute(query, values)
        conn.commit()
        if cursor.rowcount > 0:
            print(f"成功更新图书 ID: {book_id}")
        else:
            print(f"未找到图书 ID: {book_id}")
    except mysql.connector.Error as err:
        print(f"更新图书失败: {err}")
    finally:
        cursor.close()
        conn.close()
# 查询图书
def query_books(book_id=None):
    conn = connect_to_db()
    if not conn:
        return
    try:
        cursor = conn.cursor(dictionary=True)
        if book_id:
            query = "SELECT * FROM Books WHERE BookID = %s"
            cursor.execute(query, (book_id,))
        else:
            query = "SELECT * FROM Books"
            cursor.execute(query)
        books = cursor.fetchall()
        if books:
            for book in books:
                print(book)
        else:
            print("未找到图书记录")
    except mysql.connector.Error as err:
        print(f"查询图书失败: {err}")
    finally:
        cursor.close()
        conn.close()

# 测试代码
if __name__ == "__main__":
    # 添加图书
    # add_book("数理金融初步", "机械工业出版社", "Sheldon M.Ross", "2011-11-25", 30, 10)

    # 查询所有图书
    # print("所有图书记录:")
    # query_books()

    # 更新图书
    # update_book(1, Title="笑傲江湖（修订版）", Stock=15)

    # 查询单本图书
    # print("单本图书记录:")
    # query_books(36457095)

    # # 删除图书
    # delete_book(36457095)

    # 查询所有图书
    # print("所有图书记录（删除后）:")
    query_books(1002299)
