CREATE DATABASE LawFirmDB;
USE LawFirmDB;

CREATE TABLE Lawyer (
    Lawyer_id INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100),
    Bar_number VARCHAR(50),
    Specialization VARCHAR(100),
    Phone_no VARCHAR(20),
    Hourly_rate DECIMAL(10,2)
);
INSERT INTO Lawyer VALUES
(1, 'Ali Raza', 'ali@law.com', 'BAR101', 'Criminal Law', '03001234567', 5000),
(2, 'Sara Khan', 'sara@law.com', 'BAR102', 'Corporate Law', '03011234567', 7000),
(3, 'Ahmed Bilal', 'ahmed@law.com', 'BAR103', 'Family Law', '03021234567', 4500),
(4, 'Fatima Noor', 'fatima@law.com', 'BAR104', 'Civil Law', '03031234567', 6000),
(5, 'Usman Tariq', 'usman@law.com', 'BAR105', 'Tax Law', '03041234567', 8000),
(6, 'Hina Aslam', 'hina@law.com', 'BAR106', 'Property Law', '03051234567', 5500),
(7, 'Bilal Ahmed', 'bilal@law.com', 'BAR107', 'Cyber Law', '03061234567', 9000),
(8, 'Zain Malik', 'zain@law.com', 'BAR108', 'Immigration Law', '03071234567', 6500);

CREATE TABLE Judge (
    Judge_id INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Court_name VARCHAR(100),
    Specialization VARCHAR(100),
    Contact_info VARCHAR(200)
);
INSERT INTO Judge VALUES
(1, 'Justice Hamid', 'Lahore High Court', 'Criminal', 'judge1@court.com'),
(2, 'Justice Salman', 'Islamabad Court', 'Civil', 'judge2@court.com'),
(3, 'Justice Ayesha', 'Karachi Court', 'Family', 'judge3@court.com'),
(4, 'Justice Tariq', 'Faisalabad Court', 'Corporate', 'judge4@court.com'),
(5, 'Justice Imran', 'Multan Court', 'Tax', 'judge5@court.com'),
(6, 'Justice Nadia', 'Peshawar Court', 'Property', 'judge6@court.com'),
(7, 'Justice Danish', 'Supreme Court', 'Cyber', 'judge7@court.com'),
(8, 'Justice Sana', 'Rawalpindi Court', 'Immigration', 'judge8@court.com');

CREATE TABLE Client (
    Client_id INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    CNIC VARCHAR(20),
    Phone_no VARCHAR(20),
    Email VARCHAR(100),
    Street VARCHAR(100),
    City VARCHAR(100)
);
INSERT INTO Client VALUES
(1, 'Hamza Ali', '33100-1111111-1', '03111234567', 'hamza@gmail.com', 'Street 1', 'Faisalabad'),
(2, 'Areeba Noor', '33100-2222222-2', '03121234567', 'areeba@gmail.com', 'Street 2', 'Lahore'),
(3, 'Talha Ahmed', '33100-3333333-3', '03131234567', 'talha@gmail.com', 'Street 3', 'Karachi'),
(4, 'Ahmed Rauf', '33100-4444444-4', '03141234567', 'ahmed@gmail.com', 'Street 4', 'Islamabad'),
(5, 'Mehwish Fatima', '33100-5555555-5', '03151234567', 'mehwish@gmail.com', 'Street 5', 'Multan'),
(6, 'Umer Farooq', '33100-6666666-6', '03161234567', 'umer@gmail.com', 'Street 6', 'Peshawar'),
(7, 'Iqra Khalid', '33100-7777777-7', '03171234567', 'iqra@gmail.com', 'Street 7', 'Sialkot'),
(8, 'Danish Ali', '33100-8888888-8', '03181234567', 'danish@gmail.com', 'Street 8', 'Rawalpindi');

CREATE TABLE [Case] (
    Case_id INT PRIMARY KEY,
    Case_no VARCHAR(50),
    Title VARCHAR(150) NOT NULL,
    Case_type VARCHAR(100),
    Status VARCHAR(50),
    Filed_date DATE,
    Client_id INT NOT NULL,
    Judge_id INT NOT NULL,
    FOREIGN KEY (Client_id) REFERENCES Client(Client_id),
    FOREIGN KEY (Judge_id) REFERENCES Judge(Judge_id)
);
INSERT INTO [Case] VALUES
(1, 'C101', 'Property Dispute', 'Civil', 'Open', '2026-01-10', 1, 2),
(2, 'C102', 'Cyber Fraud', 'Cyber', 'Closed', '2026-01-15', 2, 7),
(3, 'C103', 'Divorce Case', 'Family', 'Pending', '2026-02-01', 3, 3),
(4, 'C104', 'Tax Evasion', 'Tax', 'Open', '2026-02-05', 4, 5),
(5, 'C105', 'Corporate Fraud', 'Corporate', 'Closed', '2026-02-12', 5, 4),
(6, 'C106', 'Immigration Appeal', 'Immigration', 'Pending', '2026-03-01', 6, 8),
(7, 'C107', 'Land Ownership', 'Property', 'Open', '2026-03-05', 7, 6),
(8, 'C108', 'Robbery Case', 'Criminal', 'Closed', '2026-03-10', 8, 1);

CREATE TABLE Case_Lawyer (
    id INT PRIMARY KEY,
    Case_id INT NOT NULL,
    Lawyer_id INT NOT NULL,
    Assigned_date DATE,
    Role VARCHAR(100),
    FOREIGN KEY (Case_id) REFERENCES [Case](Case_id),
    FOREIGN KEY (Lawyer_id) REFERENCES Lawyer(Lawyer_id)
);
INSERT INTO Case_Lawyer VALUES
(1, 1, 4, '2026-01-11', 'Lead Lawyer'),
(2, 2, 7, '2026-01-16', 'Advisor'),
(3, 3, 3, '2026-02-02', 'Lead Lawyer'),
(4, 4, 5, '2026-02-06', 'Senior Lawyer'),
(5, 5, 2, '2026-02-13', 'Corporate Advisor'),
(6, 6, 8, '2026-03-02', 'Immigration Expert'),
(7, 7, 6, '2026-03-06', 'Property Lawyer'),
(8, 8, 1, '2026-03-11', 'Criminal Lawyer');

CREATE TABLE Timeline (
    Entry_id INT PRIMARY KEY,
    Case_id INT NOT NULL,
    Hearing_date DATE,
    Next_date DATE,
    Proceeding_type VARCHAR(100),
    Outcome VARCHAR(200),
    Note VARCHAR(300),
    FOREIGN KEY (Case_id) REFERENCES [Case](Case_id)
);
INSERT INTO Timeline VALUES
(1, 1, '2026-01-20', '2026-02-01', 'Hearing', 'Pending', 'First hearing conducted'),
(2, 2, '2026-01-25', '2026-02-05', 'Evidence Review', 'Completed', 'Evidence accepted'),
(3, 3, '2026-02-10', '2026-02-20', 'Mediation', 'Pending', 'Family discussion ongoing'),
(4, 4, '2026-02-15', '2026-02-28', 'Tax Audit', 'In Progress', 'FBR documents submitted'),
(5, 5, '2026-02-20', '2026-03-01', 'Corporate Meeting', 'Completed', 'Settlement reached'),
(6, 6, '2026-03-05', '2026-03-15', 'Immigration Review', 'Pending', 'Visa papers checked'),
(7, 7, '2026-03-10', '2026-03-20', 'Land Inspection', 'In Progress', 'Site visit completed'),
(8, 8, '2026-03-15', '2026-03-25', 'Witness Hearing', 'Completed', 'Witness statements recorded');

CREATE TABLE Journal (
    Journal_id INT PRIMARY KEY,
    Case_id INT NOT NULL,
    Lawyer_id INT NOT NULL,
    Entry_date DATE,
    Entry_type VARCHAR(100),
    Content VARCHAR(500),
    FOREIGN KEY (Case_id) REFERENCES [Case](Case_id),
    FOREIGN KEY (Lawyer_id) REFERENCES Lawyer(Lawyer_id)
);
INSERT INTO Journal VALUES
(1, 1, 4, '2026-01-12', 'Case Note', 'Client submitted land documents'),
(2, 2, 7, '2026-01-18', 'Cyber Analysis', 'Fraud transaction traced'),
(3, 3, 3, '2026-02-03', 'Meeting', 'Client counseling session'),
(4, 4, 5, '2026-02-07', 'Tax Review', 'FBR notices reviewed'),
(5, 5, 2, '2026-02-14', 'Corporate Discussion', 'Company audit discussed'),
(6, 6, 8, '2026-03-03', 'Immigration Note', 'Embassy documents verified'),
(7, 7, 6, '2026-03-07', 'Inspection', 'Property ownership verified'),
(8, 8, 1, '2026-03-12', 'Criminal Report', 'Police FIR reviewed');

CREATE TABLE Evidence (
    Evidence_id INT PRIMARY KEY,
    Case_id INT NOT NULL,
    Title VARCHAR(150),
    Evidence_type VARCHAR(100),
    Description VARCHAR(300),
    Submitted_date DATE,
    File_path VARCHAR(300),
    FOREIGN KEY (Case_id) REFERENCES [Case](Case_id)
);
INSERT INTO Evidence VALUES
(1, 1, 'Land Papers', 'Document', 'Ownership documents', '2026-01-13', 'C:\Evidence\land.pdf'),
(2, 2, 'Transaction Logs', 'Digital', 'Bank transaction details', '2026-01-19', 'C:\Evidence\logs.pdf'),
(3, 3, 'Marriage Certificate', 'Document', 'Nikah certificate submitted', '2026-02-04', 'C:\Evidence\nikah.pdf'),
(4, 4, 'Tax Reports', 'Financial', 'Annual tax reports', '2026-02-08', 'C:\Evidence\tax.pdf'),
(5, 5, 'Audit Report', 'Corporate', 'Internal audit report', '2026-02-15', 'C:\Evidence\audit.pdf'),
(6, 6, 'Passport Copy', 'Document', 'Passport verification copy', '2026-03-04', 'C:\Evidence\passport.pdf'),
(7, 7, 'Registry File', 'Document', 'Land registry documents', '2026-03-08', 'C:\Evidence\registry.pdf'),
(8, 8, 'CCTV Footage', 'Video', 'Crime scene footage', '2026-03-13', 'C:\Evidence\cctv.mp4');

CREATE TABLE Payment (
    Payment_id INT PRIMARY KEY,
    Case_id INT NOT NULL,
    Lawyer_id INT NOT NULL,
    Client_id INT NOT NULL,
    Amount DECIMAL(10,2),
    Payment_date DATE,
    Status VARCHAR(50),
    Description VARCHAR(300),
    FOREIGN KEY (Case_id) REFERENCES [Case](Case_id),
    FOREIGN KEY (Lawyer_id) REFERENCES Lawyer(Lawyer_id),
    FOREIGN KEY (Client_id) REFERENCES Client(Client_id)
);
INSERT INTO Payment VALUES
(1, 1, 4, 1, 50000, '2026-01-14', 'Paid', 'Initial legal fee'),
(2, 2, 7, 2, 75000, '2026-01-20', 'Paid', 'Cyber investigation charges'),
(3, 3, 3, 3, 30000, '2026-02-05', 'Pending', 'Family case consultation'),
(4, 4, 5, 4, 90000, '2026-02-10', 'Paid', 'Tax advisory charges'),
(5, 5, 2, 5, 120000, '2026-02-16', 'Paid', 'Corporate legal services'),
(6, 6, 8, 6, 65000, '2026-03-05', 'Pending', 'Immigration processing fee'),
(7, 7, 6, 7, 45000, '2026-03-09', 'Paid', 'Property verification fee'),
(8, 8, 1, 8, 80000, '2026-03-14', 'Paid', 'Criminal defense fee');