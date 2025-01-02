CREATE DATABASE library_management;
SHOW DATABASES;
USE library_management;

-- 创建图书表
CREATE TABLE Books (
    BookID INT PRIMARY KEY AUTO_INCREMENT,
    Title VARCHAR(100) NOT NULL,
    Publisher VARCHAR(100),
    Author VARCHAR(100),
    PublicationDate DATE,
    LoanPeriod INT DEFAULT 30,
    Stock INT DEFAULT 0
);

-- 创建学生表
CREATE TABLE Students (
    StudentID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(50) NOT NULL,
    Gender ENUM('Male', 'Female'),
    DOB DATE,
    Major VARCHAR(100),
    Class VARCHAR(50),
    Department VARCHAR(100)
);



USE library_management;

-- 检查是否存在 Books 表
SHOW TABLES LIKE 'Books';

-- 检查是否存在 Students 表
SHOW TABLES LIKE 'Students';

-- 检查是否存在 BorrowRecords 表
SHOW TABLES LIKE 'BorrowRecords';
-- 查看 Books 表结构
DESCRIBE Books;

-- 查看 Students 表结构
DESCRIBE Students;

-- 查看 BorrowRecords 表结构
DESCRIBE BorrowRecords;
SELECT COUNT(*) FROM Books WHERE BookID = '1007305';
SELECT * FROM Books;
DELETE FROM Books;
SELECT * FROM Students;
SELECT * FROM BorrowRecords;
-- 创建借阅记录表
CREATE TABLE BorrowRecords (
    RecordID INT PRIMARY KEY AUTO_INCREMENT,
    BookID INT NOT NULL,
    StudentID INT NOT NULL,
    BorrowDate DATE NOT NULL,
    ReturnDate DATE DEFAULT NULL,
    DueDate DATE NOT NULL,
    FOREIGN KEY (BookID) REFERENCES Books(BookID),
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID)
);

-- 创建触发器，在插入数据时自动设置 BorrowDate 和 DueDate
DELIMITER $$

CREATE TRIGGER before_insert_borrowrecords
BEFORE INSERT ON BorrowRecords
FOR EACH ROW
BEGIN
    -- 如果 BorrowDate 未指定，设置为当前日期
    IF NEW.BorrowDate IS NULL THEN
        SET NEW.BorrowDate = CURRENT_DATE;
    END IF;

    -- 如果 DueDate 未指定，设置为 BorrowDate + 14 天
    IF NEW.DueDate IS NULL THEN
        SET NEW.DueDate = DATE_ADD(NEW.BorrowDate, INTERVAL 14 DAY);
    END IF;
END $$

DELIMITER ;
-- 清单
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
