import pymysql
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'deng1217',
    'database': 'library_management',
    'port': 3306
}
# 映射性别文本到数据库枚举值
gender_map = {'男': 'Male', '女': 'Female'}
# 读取数据文件并插入到数据库
def insert_students_from_file(file_path):
    # 连接数据库
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            student_data = []
            student = {}
            for line in lines:
                line = line.strip()
                if line.startswith("学号:"):
                    student['StudentID'] = int(line.split(":")[1].strip())
                elif line.startswith("姓名:"):
                    student['Name'] = line.split(":")[1].strip()
                elif line.startswith("性别:"):
                    gender_text = line.split(":")[1].strip()
                    student['Gender'] = gender_map.get(gender_text, None)  # 映射性别
                elif line.startswith("出生日期:"):
                    student['DOB'] = line.split(":")[1].strip()
                elif line.startswith("专业:"):
                    student['Major'] = line.split(":")[1].strip()
                elif line.startswith("班级:"):
                    student['Class'] = line.split(":")[1].strip()
                elif line.startswith("学院:"):
                    student['Department'] = line.split(":")[1].strip()
                elif line.strip() == "----------------------------------------":
                    student_data.append(student)
                    student = {}

            # 插入数据
            sql = """INSERT INTO Students 
                     (Name, Gender, DOB, Major, Class, Department)
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            for student in student_data:
                cursor.execute(sql, (
                    student['Name'],
                    student['Gender'],
                    student['DOB'],
                    student['Major'],
                    student['Class'],
                    student['Department']
                ))

        # 提交事务
        connection.commit()
        print(f"成功插入 {len(student_data)} 条学生数据！")

    except Exception as e:
        print(f"发生错误: {e}")
        connection.rollback()

    finally:
        cursor.close()
        connection.close()
file_path = r"F:\pycharm项目\测试\数据库课程设计（图书管理系统）\students_data.txt"
insert_students_from_file(file_path)
