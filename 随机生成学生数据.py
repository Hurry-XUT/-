import random
from faker import Faker
# 使用Faker库生成随机中文名字
fake = Faker('zh_CN')
# 学号的起始编号
start_id = 3220811001 #还是从1开始吧
# 学院和专业数据
colleges = ['计算机学院', '电子信息学院', '机械工程学院', '土木工程学院']
majors = {
    '计算机学院': ['计算机科学与技术', '网络工程', '软件工程'],
    '电子信息学院': ['电子信息工程', '通信工程', '自动化'],
    '机械工程学院': ['机械工程', '工业设计', '材料科学与工程'],
    '土木工程学院': ['土木工程', '建筑学', '环境工程']
}
# 性别选项
genders = ['男', '女']
# 生成学生数据
students = []
for i in range(999):
    student = {}
    student['学号'] = str(start_id + i)
    student['姓名'] = fake.name()  # 随机生成中文姓名
    student['性别'] = random.choice(genders)  # 随机性别
    student['出生日期'] = f"{random.randint(1995, 2005)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"  # 随机出生日期
    student['学院'] = random.choice(colleges)  # 随机学院
    student['专业'] = random.choice(majors[student['学院']])  # 随机专业
    student['班级'] = f"{student['学院'][:2]}{random.randint(1, 10)}班"  # 根据学院随机生成班级
    students.append(student)
# 保存学生数据到txt文件
output_file = "F:\\pycharm项目\\测试\\数据库课程设计（图书管理系统）\\students_data.txt"
with open(output_file, "w", encoding="utf-8") as f:
    for student in students:
        f.write(f"学号: {student['学号']}\n")
        f.write(f"姓名: {student['姓名']}\n")
        f.write(f"性别: {student['性别']}\n")
        f.write(f"出生日期: {student['出生日期']}\n")
        f.write(f"专业: {student['专业']}\n")
        f.write(f"学院: {student['学院']}\n")
        f.write(f"班级: {student['班级']}\n")  # 增加班级信息
        f.write("----------------------------------------\n")

print("学生数据已成功生成并保存！")
