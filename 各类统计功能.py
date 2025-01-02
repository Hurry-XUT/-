import mysql.connector


def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",       # 数据库主机名
            user="root",            # 数据库用户名
            password="deng1217", # 数据库密码
            database="library_management"  # 数据库名称
        )
        return conn
    except mysql.connector.Error as err:
        print(f"连接数据库失败: {err}")
        return None
def print_overdue_report():
    conn = connect_to_db()
    if not conn:
        return
    try:
        query = """
        SELECT 
            s.Department AS 学院,
            s.Name AS 学生姓名,
            s.StudentID AS 学号,
            b.Title AS 书名,
            br.BorrowDate AS 借阅日期,
            br.DueDate AS 应还日期,
            DATEDIFF(CURDATE(), br.DueDate) AS 超期天数
        FROM 
            BorrowRecords br
        JOIN 
            Students s ON br.StudentID = s.StudentID
        JOIN 
            Books b ON br.BookID = b.BookID
        WHERE 
            br.ReturnDate IS NULL AND CURDATE() > br.DueDate
        ORDER BY 
            s.Department, 超期天数 DESC;
        """

        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            # 按学院分组
            grouped_results = {}
            for record in results:
                department = record["学院"]
                if department not in grouped_results:
                    grouped_results[department] = []
                grouped_results[department].append(record)

            # 打印分组结果
            for department, records in grouped_results.items():
                print(f"\n学院: {department}")
                print("-" * 40)
                for record in records:
                    print(f"学生姓名: {record['学生姓名']}, 学号: {record['学号']}, 书名: {record['书名']}, "
                          f"借阅日期: {record['借阅日期']}, 应还日期: {record['应还日期']}, 超期天数: {record['超期天数']} 天")
        else:
            print("当前没有超期记录。")
    except mysql.connector.Error as err:
        print(f"查询失败: {err}")
    finally:
        cursor.close()
        conn.close()
