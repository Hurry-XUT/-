from graphviz import Digraph
def create_er_diagram():
    dot = Digraph("ER_Diagram", format="png")
    # 设置实体样式为矩形
    dot.node("Books", "Books", shape="rect", style="filled", color="lightblue")
    dot.node("Students", "Students", shape="rect", style="filled", color="lightblue")
    dot.node("BorrowRecords", "BorrowRecords", shape="rect", style="filled", color="lightblue")
    # 设置属性样式为椭圆
    dot.attr(shape="ellipse", style="filled", color="lightyellow")
    # 图书实体的属性
    dot.node("BookID", "BookID")
    dot.node("Title", "Title")
    dot.node("Publisher", "Publisher")
    dot.node("Author", "Author")
    dot.node("PublicationDate", "PublicationDate")
    dot.node("LoanPeriod", "LoanPeriod")
    dot.node("Stock", "Stock")

    # 学生实体的属性
    dot.node("StudentID", "StudentID")
    dot.node("Name", "Name")
    dot.node("Gender", "Gender")
    dot.node("DOB", "DOB")
    dot.node("Major", "Major")
    dot.node("Class", "Class")
    dot.node("Department", "Department")

    # 借阅记录实体的属性
    dot.node("RecordID", "RecordID")
    dot.node("BorrowDate", "BorrowDate")
    dot.node("DueDate", "DueDate")
    dot.node("ReturnDate", "ReturnDate")
    dot.node("Borrow", "Borrow", shape="diamond", style="filled", color="lightblue")
    # 连接实体和属性
    dot.edge("Books", "BookID")
    dot.edge("Books", "Title")
    dot.edge("Books", "Publisher")
    dot.edge("Books", "Author")
    dot.edge("Books", "PublicationDate")
    dot.edge("Books", "LoanPeriod")
    dot.edge("Books", "Stock")
    dot.edge("Students", "StudentID")
    dot.edge("Students", "Name")
    dot.edge("Students", "Gender")
    dot.edge("Students", "DOB")
    dot.edge("Students", "Major")
    dot.edge("Students", "Class")
    dot.edge("Students", "Department")
    dot.edge("BorrowRecords", "RecordID")
    dot.edge("BorrowRecords", "BorrowDate")
    dot.edge("BorrowRecords", "DueDate")
    dot.edge("BorrowRecords", "ReturnDate")
    # 连接实体和关系
    dot.edge("Books", "Borrow", label="n")
    dot.edge("Students", "Borrow", label="n")
    dot.edge("Borrow", "BorrowRecords", label="1")
    # 输出图像
    dot.render("er_diagram")
    print("E-R 图已生成，文件名为 er_diagram.png")
create_er_diagram()

