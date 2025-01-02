import mysql.connector

# 连接到数据库
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="deng1217",  # 替换为你的密码
    database="library_management"
)

cursor = db.cursor()
print("成功连接到数据库！")

# 插入数据的SQL语句
book_insert_query = """
    INSERT INTO Books (BookID, Title, Author, Publisher, PublicationDate, LoanPeriod, Stock)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

# 读取文件并处理每本书的信息
with open("F:\\pycharm项目\\测试\\数据库课程设计（图书管理系统）\\cleaned_books.txt", "r", encoding="utf-8") as file:
    book_data = {}
    for line in file:
        line = line.strip()
        if line.startswith("书籍编号"):
            book_data["BookID"] = line.split(":")[1].strip()
        elif line.startswith("书名"):
            book_data["Title"] = line.split(":")[1].strip()
        elif line.startswith("第一作者"):
            book_data["Author"] = line.split(":")[1].strip()
        elif line.startswith("出版社"):
            book_data["Publisher"] = line.split(":")[1].strip()
        elif line.startswith("出版时间"):
            publication_date = line.split(":")[1].strip()
            # 对日期进行处理，确保它符合 YYYY-MM-DD 格式
            if len(publication_date) == 7 and publication_date.count('-') == 1:  # 格式是 'YYYY-MM'
                year, month = publication_date.split("-")
                # 确保月份为两位数并补充日部分
                publication_date = f"{year}-{month.zfill(2)}-01"
            # 如果日期不符合 'YYYY-MM' 格式，做进一步处理（根据需求）
            elif len(publication_date) == 4:  # 例如只有年份 '2012'
                publication_date = f"{publication_date}-01-01"
            book_data["PublicationDate"] = publication_date
        elif line == "----------------------------------------":
            # 插入数据到数据库
            try:
                # 在插入前打印每本书的数据
                print(f"正在插入书籍: {book_data}")

                cursor.execute(book_insert_query, (
                    book_data["BookID"],
                    book_data["Title"],
                    book_data["Author"],
                    book_data["Publisher"],
                    book_data["PublicationDate"],
                    30,  # 假设默认借阅期限为30天
                    10   # 假设初始库存为10
                ))
                db.commit()
                print(f"插入成功: {book_data['Title']}")
            except mysql.connector.Error as err:
                print(f"插入数据时发生错误: {book_data['Title']} - 错误信息: {err}")
            book_data = {}  # 清空字典，准备下一本书的数据

# 关闭游标和数据库连接
cursor.close()
db.close()



