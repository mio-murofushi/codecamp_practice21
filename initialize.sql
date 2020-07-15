-- 社員管理ツール　テーブル作成

-- 社員情報テーブル作成
CREATE TABLE employee_infomation(
    id INT AUTO_INCREMENT,
    employee_id VARCHAR(100),
    employee_name VARCHAR(100),
    employee_age INT,
    gender VARCHAR(5),
    photo_id VARCHAR(100),
    adress VARCHAR(100),
    department_id VARCHAR(10),
    join_date datetime,
    leave_date datetime
    PRIMARY KEY (id)
);

-- 証明写真テーブル作成
CREATE TABLE ID_photo(
    photo_id VARCHAR(100),
    photo_name VARCHAR(100),
    PRIMARY KEY (photo_id)
);

-- 部署テーブル作成
CREATE TABLE department(
    department_id VARCHAR(10),
    department_name VARCHAR(50),
    PRIMARY KEY (department_id)
);

DELETE FROM employee_infomation:

-- 初期テーブル情報の入力
INSERT INTO employee_infomation(
    employee_id,employee_name,employee_age,gender,photo_id,adress,department_id,join_date
) VALUES
( "EMP0001", "山田太郎", 35, "男", "P00001", "〒100-1000 東京都千代田区", "D01", "2019-09-11"),
( "EMP0002", "日本花子", 27, "女", "P00002", "〒200-2000 埼玉県さいたま市", "D02", "2010-10-01"),
( "EMP0003", "東京次郎", 41, "男", "P00003", "〒300-3000 神奈川県川崎市", "D01", "2017-11-22");

INSERT INTO ID_photo(
    photo_id, photo_name
) VALUES
("P00001", "山田.jpeg"),
("P00002", "日本.png"),
("P00003", "次郎.jpeg");

INSERT INTO department(
    department_id, department_name
) VALUES 
("D01", "総務部"),
("D02", "営業部");