import mysql.connector

# 数据库连接函数
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="deng1217",
            database="library_management"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"数据库连接失败: {err}")
        return None

# 借出图书
def borrow_book(book_id, student_id):
    conn = connect_to_db()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        # 检查库存是否足够
        check_stock_query = "SELECT Stock FROM Books WHERE BookID = %s"
        cursor.execute(check_stock_query, (book_id,))
        result = cursor.fetchone()
        if not result or result[0] <= 0:  #库存为0则无法借出
            print("库存不足，无法借出该书!")
            return

        # 插入借阅记录
        borrow_query = """
            INSERT INTO BorrowRecords (BookID, StudentID)
            VALUES (%s, %s)
        """
        cursor.execute(borrow_query, (book_id, student_id))

        # 更新库存
        update_stock_query = "UPDATE Books SET Stock = Stock - 1 WHERE BookID = %s"
        cursor.execute(update_stock_query, (book_id,))

        conn.commit()
        print("图书借出成功!")
    except mysql.connector.Error as err:
        print(f"借书操作失败: {err}")
    finally:
        cursor.close()
        conn.close()

# 归还图书
def return_book(record_id):
    conn = connect_to_db()
    if not conn:
        return
    try:
        cursor = conn.cursor()

        # 获取归还记录的 BookID
        get_book_query = "SELECT BookID FROM BorrowRecords WHERE RecordID = %s"
        cursor.execute(get_book_query, (record_id,))
        result = cursor.fetchone()
        if not result:
            print("未找到借阅记录!")
            return

        book_id = result[0]
        # 更新归还日期
        update_return_date_query = "UPDATE BorrowRecords SET ReturnDate = CURRENT_DATE WHERE RecordID = %s"
        cursor.execute(update_return_date_query, (record_id,))
        # 更新库存
        update_stock_query = "UPDATE Books SET Stock = Stock + 1 WHERE BookID = %s"
        cursor.execute(update_stock_query, (book_id,))

        conn.commit()
        print("图书归还成功!")
    except mysql.connector.Error as err:
        print(f"还书操作失败: {err}")
    finally:
        cursor.close()
        conn.close()


# 修改借阅记录
def update_borrow_record(record_id, new_return_date=None, new_due_date=None):
    conn = connect_to_db()
    if not conn:
        return
    try:
        cursor = conn.cursor()

        # 构建动态更新语句
        update_fields = []
        values = []

        if new_return_date:
            update_fields.append("ReturnDate = %s")
            values.append(new_return_date)
        if new_due_date:
            update_fields.append("DueDate = %s")
            values.append(new_due_date)

        if not update_fields:
            print("未提供要更新的字段！")
            return

        update_query = f"""
            UPDATE BorrowRecords 
            SET {', '.join(update_fields)}
            WHERE RecordID = %s
        """
        values.append(record_id)
        cursor.execute(update_query, tuple(values))

        conn.commit()
        print(f"借阅记录 {record_id} 更新成功!")
    except mysql.connector.Error as err:
        print(f"更新借阅记录失败: {err}")
    finally:
        cursor.close()
        conn.close()
# 示例调用：将记录ID为2的借阅记录归还日期更新为2024-12-09
# 查询借阅记录
def query_borrow_records(record_id=None):
    conn = connect_to_db()
    if not conn:
        return
    try:
        cursor = conn.cursor(dictionary=True)
        if record_id:
            query = "SELECT * FROM BorrowRecords WHERE RecordID = %s"
            cursor.execute(query, (record_id,))
        else:
            query = "SELECT * FROM BorrowRecords"
            cursor.execute(query)
        records = cursor.fetchall()
        if records:
            for record in records:
                print(record)
        else:
            print("未找到借阅记录")
    except mysql.connector.Error as err:
        print(f"查询借阅记录失败: {err}")
    finally:
        cursor.close()
        conn.close()

# 删除借阅记录
def delete_borrow_record(record_id):
    conn = connect_to_db()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        # 检查记录是否存在
        check_record_query = "SELECT BookID FROM BorrowRecords WHERE RecordID = %s"
        cursor.execute(check_record_query, (record_id,))
        result = cursor.fetchone()
        if not result:
            print("未找到借阅记录!")
            return

        book_id = result[0]

        # 删除记录
        delete_query = "DELETE FROM BorrowRecords WHERE RecordID = %s"
        cursor.execute(delete_query, (record_id,))

        # 恢复库存
        update_stock_query = "UPDATE Books SET Stock = Stock + 1 WHERE BookID = %s"
        cursor.execute(update_stock_query, (book_id,))

        conn.commit()
        print("借阅记录删除成功!")
    except mysql.connector.Error as err:
        print(f"删除借阅记录失败: {err}")
    finally:
        cursor.close()
        conn.close()
# borrow_book(1002299, 5)  # 借出书籍ID为1002299，学生ID为2
# query_borrow_records()  # 查询所有借阅记录
# # query_borrow_records(1)  # 查询记录ID为1的借阅记录
# # return_book(2)
# update_borrow_record(record_id=3, new_return_date="2025-1-18")
query_borrow_records()  # 查询所有借阅记录