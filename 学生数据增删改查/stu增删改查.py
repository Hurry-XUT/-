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
# 插入学生信息
def insert_student(name, gender, dob, major, student_class, department):
    conn = connect_to_db()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        insert_query = """
            INSERT INTO Students (Name, Gender, DOB, Major, Class, Department)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (name, gender, dob, major, student_class, department))
        conn.commit()
        print("学生信息插入成功!")
    except mysql.connector.Error as err:
        print(f"插入学生信息失败: {err}")
    finally:
        cursor.close()
        conn.close()
# 删除学生信息
def delete_student(student_id):
    conn = connect_to_db()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        delete_query = "DELETE FROM Students WHERE StudentID = %s"
        cursor.execute(delete_query, (student_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print("学生信息删除成功!")
        else:
            print("未找到指定学生信息!")
    except mysql.connector.Error as err:
        print(f"删除学生信息失败: {err}")
    finally:
        cursor.close()
        conn.close()
# 更新学生信息
def update_student(student_id, name=None, gender=None, dob=None, major=None, student_class=None, department=None):
    conn = connect_to_db()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        update_query = "UPDATE Students SET"
        update_fields = []
        update_values = []

        if name:
            update_fields.append("Name = %s")
            update_values.append(name)
        if gender:
            update_fields.append("Gender = %s")
            update_values.append(gender)
        if dob:
            update_fields.append("DOB = %s")
            update_values.append(dob)
        if major:
            update_fields.append("Major = %s")
            update_values.append(major)
        if student_class:
            update_fields.append("Class = %s")
            update_values.append(student_class)
        if department:
            update_fields.append("Department = %s")
            update_values.append(department)

        if not update_fields:
            print("未提供需要更新的字段!")
            return
        update_query += ", ".join(update_fields) + " WHERE StudentID = %s"
        update_values.append(student_id)

        cursor.execute(update_query, update_values)
        conn.commit()
        if cursor.rowcount > 0:
            print("学生信息更新成功!")
        else:
            print("未找到指定学生信息!")
    except mysql.connector.Error as err:
        print(f"更新学生信息失败: {err}")
    finally:
        cursor.close()
        conn.close()
# 查询学生信息
def query_students(student_id=None):
    conn = connect_to_db()
    if not conn:
        return
    try:
        cursor = conn.cursor(dictionary=True)
        if student_id:
            query = "SELECT * FROM Students WHERE StudentID = %s"
            cursor.execute(query, (student_id,))
        else:
            query = "SELECT * FROM Students"
            cursor.execute(query)
        students = cursor.fetchall()
        if students:
            for student in students:
                print(student)
        else:
            print("未找到学生记录")
    except mysql.connector.Error as err:
        print(f"查询学生失败: {err}")
    finally:
        cursor.close()
        conn.close()
query_students(1)