import requests
from bs4 import BeautifulSoup
# 设置请求头，模拟浏览器访问
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
# 保存文件路径
file_path = r"F:\pycharm项目\测试\数据库课程设计（图书管理系统）\douban_books.txt"
# 打开文件以写入数据
with open(file_path, 'w', encoding='utf-8') as file:
    # 遍历所有分页，每页25条数据，最多抓取250条数据
    for page_start in range(0, 250, 25):
        url = f"https://book.douban.com/top250?start={page_start}"
        # 发送请求并获取页面内容
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(f"抓取第{page_start // 25 + 1}页成功！")
            soup = BeautifulSoup(response.text, 'html.parser')
            # 获取所有书籍条目
            books = soup.find_all('tr', class_='item')

            # 遍历每一本书，提取信息
            for book in books:
                # 书籍编号：从 <a href="https://book.douban.com/subject/1007305/">
                book_link = book.find('a', class_='nbg')['href']
                book_id = book_link.split('/')[-2]  # 提取编号，如 1007305
                # 书名：从 <a title="红楼梦">
                book_title = book.find('a', title=True).get_text(strip=True)
                # 出版社、第一作者和出版时间：从 <p class="pl">
                book_info = book.find('p', class_='pl').get_text(strip=True)
                # 分割文本，提取出版社、作者、出版时间等
                book_info_parts = book_info.split(' / ')
                if len(book_info_parts) >= 4:
                    author = book_info_parts[0]  # 第一作者
                    publisher = book_info_parts[1]  # 出版社
                    publish_date = book_info_parts[2]  # 出版时间
                else:
                    author = publisher = publish_date = "未知"
                # 将抓取的信息写入文件
                file.write(f"书籍编号: {book_id}\n")
                file.write(f"书名: {book_title}\n")
                file.write(f"第一作者: {author}\n")
                file.write(f"出版社: {publisher}\n")
                file.write(f"出版时间: {publish_date}\n")
                file.write("-" * 40 + "\n")
        else:
            print(f"请求失败，状态码: {response.status_code}")

print(f"所有书籍信息已保存到: {file_path}")




