def clean_book_data(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
        book_data = {}
        for line in infile:
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

                # 如果出版时间包含出版社名（如"南海出版公司"），进行特殊处理
                if "出版公司" in publication_date:
                    # 将出版时间修改为 "2024-12-31"，并将出版社名称移至 Publisher 字段
                    book_data["PublicationDate"] = "2024-12-31"
                    book_data["Publisher"] = publication_date.strip()  # 将出版社名称放入 Publisher 字段
                    print(f"警告：'{book_data['Title']}' 出版时间字段存在问题，已设置为 '2024-12-31'，出版社更新为 '{book_data['Publisher']}'。")
                elif len(publication_date) == 7 and publication_date.count('-') == 1:  # 格式是 'YYYY-MM'
                    year, month = publication_date.split("-")
                    book_data["PublicationDate"] = f"{year}-{month.zfill(2)}-01"
                # 如果日期不符合 'YYYY-MM' 格式，做进一步处理（根据需求）
                elif len(publication_date) == 4:  # 例如只有年份 '2012'
                    book_data["PublicationDate"] = f"{publication_date}-01-01"
                else:
                    book_data["PublicationDate"] = "2024-12-31"  # 如果格式不正确，给一个默认日期

            elif line == "----------------------------------------":
                # 检查是否有有效的出版时间，如果没有，设为默认日期
                if "PublicationDate" not in book_data:
                    book_data["PublicationDate"] = "2024-12-31"  # 如果没有出版时间，默认给一个日期

                # 输出清洗后的数据
                cleaned_data = f"书籍编号: {book_data['BookID']}\n"
                cleaned_data += f"书名: {book_data['Title']}\n"
                cleaned_data += f"第一作者: {book_data['Author']}\n"
                cleaned_data += f"出版社: {book_data['Publisher']}\n"
                cleaned_data += f"出版时间: {book_data['PublicationDate']}\n"
                cleaned_data += "-" * 40 + "\n"
                outfile.write(cleaned_data)
                book_data = {}  # 清空字典，准备下一本书的数据

    print(f"数据清洗完毕，清洗后的数据已保存到 {output_file}.")

# 输入和输出文件路径
input_file = "F:\\pycharm项目\\测试\\数据库课程设计（图书管理系统）\\douban_books.txt"
output_file = "F:\\pycharm项目\\测试\\数据库课程设计（图书管理系统）\\cleaned_books.txt"

# 清洗数据
clean_book_data(input_file, output_file)


