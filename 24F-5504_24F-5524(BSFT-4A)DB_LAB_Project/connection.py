import pyodbc
#,connection functions
connection = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=HadiaLaraib\\SQLEXPRESS;"
    "DATABASE=master;"
    "Trusted_Connection=yes;"
)

cursor = connection.cursor()

print("Database Connected Successfully")

cursor.execute("""
CREATE OR ALTER PROCEDURE get_timeline_entry_by_id
    @Entry_id INT
AS
BEGIN
    SELECT * FROM Timeline WHERE Entry_id = @Entry_id
END
""")

cursor.execute("""
CREATE OR ALTER PROCEDURE get_journal_by_id
    @Journal_id INT
AS
BEGIN
    SELECT * FROM Journal WHERE Journal_id = @Journal_id
END
""")

cursor.execute("""
CREATE OR ALTER PROCEDURE get_evidence_by_id
    @Evidence_id INT
AS
BEGIN
    SELECT * FROM Evidence WHERE Evidence_id = @Evidence_id
END
""")

cursor.execute("""
CREATE OR ALTER PROCEDURE get_payment_by_id
    @Payment_id INT
AS
BEGIN
    SELECT * FROM Payment WHERE Payment_id = @Payment_id
END
""")

cursor.execute("""
CREATE OR ALTER PROCEDURE get_judge_by_name
    @Name VARCHAR(100)
AS
BEGIN
    SELECT * FROM Judge WHERE Name = @Name
END
""")

cursor.execute("""
CREATE OR ALTER PROCEDURE get_client_by_name
    @Name VARCHAR(100)
AS
BEGIN
    SELECT * FROM Client WHERE Name = @Name
END
""")

cursor.execute("""
CREATE OR ALTER PROCEDURE get_lawyer_by_name
    @Name VARCHAR(100)
AS
BEGIN
    SELECT * FROM Lawyer WHERE Name = @Name
END
""")

cursor.execute("""
CREATE OR ALTER PROCEDURE get_assignment_by_id
    @id INT
AS
BEGIN
    SELECT * FROM Case_Lawyer WHERE id = @id
END
""")

cursor.execute("""
CREATE OR ALTER PROCEDURE add_case
    @Case_id INT,
    @Case_no VARCHAR(50),
    @Client_id INT,
    @Judge_id INT,
    @Title VARCHAR(150),
    @Case_type VARCHAR(100),
    @Status VARCHAR(50),
    @Filed_date DATE
AS
BEGIN
    IF EXISTS (SELECT * FROM [Case] WHERE Case_id = @Case_id)
    BEGIN
        PRINT 'Error: Case ID already exists.';
        RETURN;
    END
    INSERT INTO [Case] (Case_id, Case_no, Title, Case_type, Status, Filed_date, Client_id, Judge_id)
    VALUES (@Case_id, @Case_no, @Title, @Case_type, @Status, @Filed_date, @Client_id, @Judge_id);
    PRINT 'Case added successfully.';
END
""")

cursor.execute("""
CREATE OR ALTER PROCEDURE update_case
    @Case_id INT,
    @Case_no VARCHAR(50),
    @Client_id INT,
    @Judge_id INT,
    @Title VARCHAR(150),
    @Case_type VARCHAR(100),
    @Status VARCHAR(50),
    @Filed_date DATE
AS
BEGIN
    IF EXISTS (SELECT * FROM [Case] WHERE Case_id = @Case_id)
    BEGIN
        UPDATE [Case]
        SET Case_no = @Case_no,
            Title = @Title,
            Case_type = @Case_type,
            Status = @Status,
            Filed_date = @Filed_date,
            Client_id = @Client_id,
            Judge_id = @Judge_id
        WHERE Case_id = @Case_id;
        PRINT 'Case updated successfully.';
    END
    ELSE
    BEGIN
        PRINT 'Error: Case does not exist.';
    END
END
""")

cursor.execute("""
CREATE OR ALTER PROCEDURE update_client
    @Client_id INT,
    @Name VARCHAR(100),
    @CNIC VARCHAR(20),
    @Phone_no VARCHAR(20),
    @Email VARCHAR(100),
    @Street VARCHAR(100),
    @City VARCHAR(100)
AS
BEGIN
    IF EXISTS (SELECT * FROM Client WHERE Client_id = @Client_id)
    BEGIN
        UPDATE Client
        SET Name = @Name,
            CNIC = @CNIC,
            Phone_no = @Phone_no,
            Email = @Email,
            Street = @Street,
            City = @City
        WHERE Client_id = @Client_id;
        PRINT 'Client updated successfully.';
    END
    ELSE
    BEGIN
        PRINT 'Error: Client does not exist.';
    END
END
""")

cursor.execute("""
CREATE OR ALTER PROCEDURE get_case_by_title
    @Title VARCHAR(150)
AS
BEGIN
    SELECT * FROM [Case] WHERE Title = @Title
END
""")

cursor.execute("""
CREATE OR ALTER PROCEDURE get_evidence_by_title
    @Title VARCHAR(150)
AS
BEGIN
    SELECT * FROM Evidence WHERE Title = @Title
END
""")

connection.commit()


# Validation Functions

def is_valid_id(value):
    if value <= 0:
        return False
    return True

def is_not_empty(value):
    if value.strip() == "":
        return False
    return True

def is_valid_date(value):
    parts = value.split("-")
    if len(parts) != 3:
        return False
    if len(parts[0]) != 4 or len(parts[1]) != 2 or len(parts[2]) != 2:
        return False
    if not parts[0].isdigit() or not parts[1].isdigit() or not parts[2].isdigit():
        return False
    return True

def is_valid_email(value):
    if "@" not in value or "." not in value:
        return False
    return True

def is_valid_phone(value):
    if not value.isdigit():
        return False
    if len(value) < 10 or len(value) > 15:
        return False
    return True

def is_valid_cnic(value):
    parts = value.split("-")
    if len(parts) != 3:
        return False
    if len(parts[0]) != 5 or len(parts[1]) != 7 or len(parts[2]) != 1:
        return False
    if not parts[0].isdigit() or not parts[1].isdigit() or not parts[2].isdigit():
        return False
    return True

def is_valid_amount(value):
    if value <= 0:
        return False
    return True

def is_valid_name(value):
    if value.strip() == "":
        return False
    for char in value:
        if not char.isalpha() and char != " ":
            return False
    return True

def record_exists(proc, param_name, value):
    try:
        cursor.execute(f"EXEC {proc} {param_name}=?", (value,))
        rows = fetch_rows()
        return len(rows) > 0
    except pyodbc.ProgrammingError:
        return False

def fetch_rows():
    try:
        return cursor.fetchall()
    except pyodbc.ProgrammingError:
        return []

def lawyer_assigned_to_case(case_id, lawyer_id):
    try:
        cursor.execute("SELECT * FROM Case_Lawyer WHERE Case_id=? AND Lawyer_id=?", (case_id, lawyer_id))
        return len(cursor.fetchall()) > 0
    except:
        return False

def client_belongs_to_case(case_id, client_id):
    try:
        cursor.execute("SELECT * FROM [Case] WHERE Case_id=? AND Client_id=?", (case_id, client_id))
        return len(cursor.fetchall()) > 0
    except:
        return False

def judge_assigned_to_case(case_id, judge_id):
    try:
        cursor.execute("SELECT * FROM [Case] WHERE Case_id=? AND Judge_id=?", (case_id, judge_id))
        return len(cursor.fetchall()) > 0
    except:
        return False

#real program
class Judge:

    def add_judge(self):

        try:
            judge_id = int(input("Enter Judge ID: "))
        except ValueError:
            print("Error: Judge ID must be a number.")
            return
        if not is_valid_id(judge_id):
            print("Error: Judge ID must be a positive number.")
            return
        if record_exists("get_judge_by_id", "@Judge_id", judge_id):
            print("Error: Judge with this ID already exists.")
            return

        name = input("Enter Judge Name: ")
        if not is_valid_name(name):
            print("Error: Judge Name must contain only letters and spaces.")
            return
        if record_exists("get_judge_by_name", "@Name", name):
            print("Error: A judge with this name already exists.")
            return

        court_name = input("Enter Court Name: ")
        if not is_valid_name(court_name):
            print("Error: Court Name must contain only letters and spaces.")
            return

        contact_info = input("Enter Contact Info (Email): ")
        if not is_valid_email(contact_info):
            print("Error: Contact Info must be a valid email containing '@' and '.'.")
            return

        specialization = input("Enter Specialization: ")
        if not is_valid_name(specialization):
            print("Error: Specialization must contain only letters and spaces.")
            return

        cursor.execute(
            """
            EXEC add_judge
                @Judge_id=?,
                @Name=?,
                @Court_name=?,
                @Contact_info=?,
                @Specialization=?
            """,
            (judge_id, name, court_name, contact_info, specialization)
        )
        connection.commit()
        print("Judge added successfully.")

    def get_all_judges(self):

        cursor.execute("EXEC get_all_judges")
        rows = fetch_rows()

        if len(rows) == 0:
            print("No judges found.")
        else:
            for row in rows:
                print(row)

    def get_judge_by_id(self):

        try:
            judge_id = int(input("Enter Judge ID: "))
        except ValueError:
            print("Error: Judge ID must be a number.")
            return
        if not is_valid_id(judge_id):
            print("Error: Judge ID must be a positive number.")
            return

        cursor.execute("EXEC get_judge_by_id @Judge_id=?", (judge_id,))
        rows = fetch_rows()

        if len(rows) == 0:
            print("Error: Judge does not exist.")
        else:
            for row in rows:
                print(row)

    def update_judge(self):

        try:
            judge_id = int(input("Enter Judge ID to update: "))
        except ValueError:
            print("Error: Judge ID must be a number.")
            return
        if not is_valid_id(judge_id):
            print("Error: Judge ID must be a positive number.")
            return
        if not record_exists("get_judge_by_id", "@Judge_id", judge_id):
            print("Error: Judge with this ID does not exist.")
            return

        name = input("Enter New Judge Name: ")
        if not is_valid_name(name):
            print("Error: Judge Name must contain only letters and spaces.")
            return

        court_name = input("Enter New Court Name: ")
        if not is_valid_name(court_name):
            print("Error: Court Name must contain only letters and spaces.")
            return

        contact_info = input("Enter New Contact Info (Email): ")
        if not is_valid_email(contact_info):
            print("Error: Contact Info must be a valid email containing '@' and '.'.")
            return

        specialization = input("Enter New Specialization: ")
        if not is_valid_name(specialization):
            print("Error: Specialization must contain only letters and spaces.")
            return

        cursor.execute(
            """
            EXEC update_judge
                @Judge_id=?,
                @Name=?,
                @Court_name=?,
                @Contact_info=?,
                @Specialization=?
            """,
            (judge_id, name, court_name, contact_info, specialization)
        )
        connection.commit()
        print("Judge updated successfully.")

    def delete_judge(self):

        try:
            judge_id = int(input("Enter Judge ID to delete: "))
        except ValueError:
            print("Error: Judge ID must be a number.")
            return
        if not is_valid_id(judge_id):
            print("Error: Judge ID must be a positive number.")
            return
        if not record_exists("get_judge_by_id", "@Judge_id", judge_id):
            print("Error: Judge with this ID does not exist.")
            return

        cursor.execute("EXEC delete_judge @Judge_id=?", (judge_id,))
        connection.commit()
        print("Judge deleted successfully.")


class Client:

    def add_client(self):

        try:
            client_id = int(input("Enter Client ID: "))
        except ValueError:
            print("Error: Client ID must be a number.")
            return
        if not is_valid_id(client_id):
            print("Error: Client ID must be a positive number.")
            return
        if record_exists("get_client_by_id", "@Client_id", client_id):
            print("Error: Client with this ID already exists.")
            return

        name = input("Enter Client Name: ")
        if not is_valid_name(name):
            print("Error: Client Name must contain only letters and spaces.")
            return
        if record_exists("get_client_by_name", "@Name", name):
            print("Error: A client with this name already exists.")
            return

        cnic = input("Enter CNIC (format: XXXXX-XXXXXXX-X): ")
        if not is_valid_cnic(cnic):
            print("Error: CNIC must be in format XXXXX-XXXXXXX-X.")
            return

        phone_no = input("Enter Phone Number (digits only, 10-15 digits): ")
        if not is_valid_phone(phone_no):
            print("Error: Phone number must contain only digits and be 10-15 digits long.")
            return

        email = input("Enter Email: ")
        if not is_valid_email(email):
            print("Error: Email must contain '@' and '.'.")
            return

        street = input("Enter Street: ")
        if not is_not_empty(street):
            print("Error: Street cannot be empty.")
            return

        city = input("Enter City: ")
        if not is_valid_name(city):
            print("Error: City must contain only letters and spaces.")
            return

        cursor.execute(
            """
            EXEC add_client
                @Client_id=?,
                @Name=?,
                @CNIC=?,
                @Phone_no=?,
                @Email=?,
                @Street=?,
                @City=?
            """,
            (client_id, name, cnic, phone_no, email, street, city)
        )
        connection.commit()
        print("Client added successfully.")

    def get_all_clients(self):

        cursor.execute("EXEC get_all_clients")
        rows = fetch_rows()

        if len(rows) == 0:
            print("No clients found.")
        else:
            for row in rows:
                print(row)

    def get_client_by_id(self):

        try:
            client_id = int(input("Enter Client ID: "))
        except ValueError:
            print("Error: Client ID must be a number.")
            return
        if not is_valid_id(client_id):
            print("Error: Client ID must be a positive number.")
            return

        cursor.execute("EXEC get_client_by_id @Client_id=?", (client_id,))
        rows = fetch_rows()

        if len(rows) == 0:
            print("Error: Client does not exist.")
        else:
            for row in rows:
                print(row)

    def update_client(self):

        try:
            client_id = int(input("Enter Client ID to update: "))
        except ValueError:
            print("Error: Client ID must be a number.")
            return
        if not is_valid_id(client_id):
            print("Error: Client ID must be a positive number.")
            return
        if not record_exists("get_client_by_id", "@Client_id", client_id):
            print("Error: Client with this ID does not exist.")
            return

        name = input("Enter New Client Name: ")
        if not is_valid_name(name):
            print("Error: Client Name must contain only letters and spaces.")
            return

        cnic = input("Enter New CNIC (format: XXXXX-XXXXXXX-X): ")
        if not is_valid_cnic(cnic):
            print("Error: CNIC must be in format XXXXX-XXXXXXX-X.")
            return

        phone_no = input("Enter New Phone Number (digits only, 10-15 digits): ")
        if not is_valid_phone(phone_no):
            print("Error: Phone number must contain only digits and be 10-15 digits long.")
            return

        email = input("Enter New Email: ")
        if not is_valid_email(email):
            print("Error: Email must contain '@' and '.'.")
            return

        street = input("Enter New Street: ")
        if not is_not_empty(street):
            print("Error: Street cannot be empty.")
            return

        city = input("Enter New City: ")
        if not is_valid_name(city):
            print("Error: City must contain only letters and spaces.")
            return

        cursor.execute(
            """
            EXEC update_client
                @Client_id=?,
                @Name=?,
                @CNIC=?,
                @Phone_no=?,
                @Email=?,
                @Street=?,
                @City=?
            """,
            (client_id, name, cnic, phone_no, email, street, city)
        )
        connection.commit()
        print("Client updated successfully.")

    def delete_client(self):

        try:
            client_id = int(input("Enter Client ID to delete: "))
        except ValueError:
            print("Error: Client ID must be a number.")
            return
        if not is_valid_id(client_id):
            print("Error: Client ID must be a positive number.")
            return
        if not record_exists("get_client_by_id", "@Client_id", client_id):
            print("Error: Client with this ID does not exist.")
            return

        cursor.execute("EXEC delete_client @Client_id=?", (client_id,))
        connection.commit()
        print("Client deleted successfully.")


class Lawyer:

    def add_lawyer(self):

        try:
            lawyer_id = int(input("Enter Lawyer ID: "))
        except ValueError:
            print("Error: Lawyer ID must be a number.")
            return
        if not is_valid_id(lawyer_id):
            print("Error: Lawyer ID must be a positive number.")
            return
        if record_exists("get_lawyer_by_id", "@Lawyer_id", lawyer_id):
            print("Error: Lawyer with this ID already exists.")
            return

        name = input("Enter Lawyer Name: ")
        if not is_valid_name(name):
            print("Error: Lawyer Name must contain only letters and spaces.")
            return
        if record_exists("get_lawyer_by_name", "@Name", name):
            print("Error: A lawyer with this name already exists.")
            return

        specialization = input("Enter Specialization: ")
        if not is_valid_name(specialization):
            print("Error: Specialization must contain only letters and spaces.")
            return

        phone_no = input("Enter Phone Number (digits only, 10-15 digits): ")
        if not is_valid_phone(phone_no):
            print("Error: Phone number must contain only digits and be 10-15 digits long.")
            return

        email = input("Enter Email: ")
        if not is_valid_email(email):
            print("Error: Email must contain '@' and '.'.")
            return

        bar_number = input("Enter Bar Number: ")
        if not is_not_empty(bar_number):
            print("Error: Bar Number cannot be empty.")
            return

        try:
            hourly_rate = float(input("Enter Hourly Rate: "))
        except ValueError:
            print("Error: Hourly Rate must be a number.")
            return
        if not is_valid_amount(hourly_rate):
            print("Error: Hourly Rate must be greater than 0.")
            return

        cursor.execute(
            """
            EXEC add_lawyer
                @Lawyer_id=?,
                @Name=?,
                @Specialization=?,
                @Phone_no=?,
                @Email=?,
                @Bar_number=?,
                @Hourly_rate=?
            """,
            (lawyer_id, name, specialization, phone_no, email, bar_number, hourly_rate)
        )
        connection.commit()
        print("Lawyer added successfully.")

    def get_all_lawyers(self):

        cursor.execute("EXEC get_all_lawyers")
        rows = fetch_rows()

        if len(rows) == 0:
            print("No lawyers found.")
        else:
            for row in rows:
                print(row)

    def get_lawyer_by_id(self):

        try:
            lawyer_id = int(input("Enter Lawyer ID: "))
        except ValueError:
            print("Error: Lawyer ID must be a number.")
            return
        if not is_valid_id(lawyer_id):
            print("Error: Lawyer ID must be a positive number.")
            return

        cursor.execute("EXEC get_lawyer_by_id @Lawyer_id=?", (lawyer_id,))
        rows = fetch_rows()

        if len(rows) == 0:
            print("Error: Lawyer does not exist.")
        else:
            for row in rows:
                print(row)

    def update_lawyer(self):

        try:
            lawyer_id = int(input("Enter Lawyer ID to update: "))
        except ValueError:
            print("Error: Lawyer ID must be a number.")
            return
        if not is_valid_id(lawyer_id):
            print("Error: Lawyer ID must be a positive number.")
            return
        if not record_exists("get_lawyer_by_id", "@Lawyer_id", lawyer_id):
            print("Error: Lawyer with this ID does not exist.")
            return

        name = input("Enter New Lawyer Name: ")
        if not is_valid_name(name):
            print("Error: Lawyer Name must contain only letters and spaces.")
            return

        specialization = input("Enter New Specialization: ")
        if not is_valid_name(specialization):
            print("Error: Specialization must contain only letters and spaces.")
            return

        phone_no = input("Enter New Phone Number (digits only, 10-15 digits): ")
        if not is_valid_phone(phone_no):
            print("Error: Phone number must contain only digits and be 10-15 digits long.")
            return

        email = input("Enter New Email: ")
        if not is_valid_email(email):
            print("Error: Email must contain '@' and '.'.")
            return

        bar_number = input("Enter New Bar Number: ")
        if not is_not_empty(bar_number):
            print("Error: Bar Number cannot be empty.")
            return

        try:
            hourly_rate = float(input("Enter New Hourly Rate: "))
        except ValueError:
            print("Error: Hourly Rate must be a number.")
            return
        if not is_valid_amount(hourly_rate):
            print("Error: Hourly Rate must be greater than 0.")
            return

        cursor.execute(
            """
            EXEC update_lawyer
                @Lawyer_id=?,
                @Name=?,
                @Specialization=?,
                @Phone_no=?,
                @Email=?,
                @Bar_number=?,
                @Hourly_rate=?
            """,
            (lawyer_id, name, specialization, phone_no, email, bar_number, hourly_rate)
        )
        connection.commit()
        print("Lawyer updated successfully.")

    def delete_lawyer(self):

        try:
            lawyer_id = int(input("Enter Lawyer ID to delete: "))
        except ValueError:
            print("Error: Lawyer ID must be a number.")
            return
        if not is_valid_id(lawyer_id):
            print("Error: Lawyer ID must be a positive number.")
            return
        if not record_exists("get_lawyer_by_id", "@Lawyer_id", lawyer_id):
            print("Error: Lawyer with this ID does not exist.")
            return

        cursor.execute("EXEC delete_lawyer @Lawyer_id=?", (lawyer_id,))
        connection.commit()
        print("Lawyer deleted successfully.")


class Case:

    def add_case(self):

        try:
            case_id = int(input("Enter Case ID: "))
        except ValueError:
            print("Error: Case ID must be a number.")
            return
        if not is_valid_id(case_id):
            print("Error: Case ID must be a positive number.")
            return
        if record_exists("get_case_by_id", "@Case_id", case_id):
            print("Error: Case with this ID already exists.")
            return

        try:
            client_id = int(input("Enter Client ID: "))
        except ValueError:
            print("Error: Client ID must be a number.")
            return
        if not is_valid_id(client_id):
            print("Error: Client ID must be a positive number.")
            return
        if not record_exists("get_client_by_id", "@Client_id", client_id):
            print("Error: Client with this ID does not exist.")
            return

        try:
            judge_id = int(input("Enter Judge ID: "))
        except ValueError:
            print("Error: Judge ID must be a number.")
            return
        if not is_valid_id(judge_id):
            print("Error: Judge ID must be a positive number.")
            return
        if not record_exists("get_judge_by_id", "@Judge_id", judge_id):
            print("Error: Judge with this ID does not exist.")
            return

        case_no = input("Enter Case No (digits only, e.g. 101): ")
        if not case_no.isdigit():
            print("Error: Case No must contain digits only.")
            return

        title = input("Enter Case Name: ")
        if not is_not_empty(title):
            print("Error: Case Name cannot be empty.")
            return
        if record_exists("get_case_by_title", "@Title", title):
            print("Error: A case with this name already exists.")
            return

        case_type = input("Enter Case Type: ")
        if not is_valid_name(case_type):
            print("Error: Case Type must contain only letters and spaces.")
            return

        status = input("Enter Case Status: ")
        if not is_valid_name(status):
            print("Error: Case Status must contain only letters and spaces.")
            return

        filed_date = input("Enter Filed Date (YYYY-MM-DD): ")
        if not is_valid_date(filed_date):
            print("Error: Filed Date must be in YYYY-MM-DD format.")
            return

        cursor.execute(
            """
            EXEC add_case
                @Case_id=?,
                @Case_no=?,
                @Client_id=?,
                @Judge_id=?,
                @Title=?,
                @Case_type=?,
                @Status=?,
                @Filed_date=?
            """,
            (case_id, case_no, client_id, judge_id, title, case_type, status, filed_date)
        )
        connection.commit()
        print("Case added successfully.")

    def get_all_cases(self):

        cursor.execute("EXEC get_all_cases")
        rows = fetch_rows()

        if len(rows) == 0:
            print("No cases found.")
        else:
            for row in rows:
                print(row)

    def get_case_by_id(self):

        try:
            case_id = int(input("Enter Case ID: "))
        except ValueError:
            print("Error: Case ID must be a number.")
            return
        if not is_valid_id(case_id):
            print("Error: Case ID must be a positive number.")
            return

        cursor.execute("EXEC get_case_by_id @Case_id=?", (case_id,))
        rows = fetch_rows()

        if len(rows) == 0:
            print("Error: Case does not exist.")
        else:
            for row in rows:
                print(row)

    def get_cases_by_client(self):

        try:
            client_id = int(input("Enter Client ID: "))
        except ValueError:
            print("Error: Client ID must be a number.")
            return
        if not is_valid_id(client_id):
            print("Error: Client ID must be a positive number.")
            return
        if not record_exists("get_client_by_id", "@Client_id", client_id):
            print("Error: Client with this ID does not exist.")
            return

        cursor.execute("EXEC get_cases_by_client @Client_id=?", (client_id,))
        rows = fetch_rows()

        if len(rows) == 0:
            print("Error: No case found for this client.")
        else:
            for row in rows:
                print(row)

    def get_cases_by_status(self):

        status = input("Enter Case Status: ")
        if not is_valid_name(status):
            print("Error: Status must contain only letters and spaces.")
            return

        cursor.execute("EXEC get_cases_by_status @Status=?", (status,))
        rows = fetch_rows()

        if len(rows) == 0:
            print("Error: No case found with this status.")
        else:
            for row in rows:
                print(row)

    def update_case(self):

        try:
            case_id = int(input("Enter Case ID to update: "))
        except ValueError:
            print("Error: Case ID must be a number.")
            return
        if not is_valid_id(case_id):
            print("Error: Case ID must be a positive number.")
            return
        if not record_exists("get_case_by_id", "@Case_id", case_id):
            print("Error: Case with this ID does not exist.")
            return

        try:
            client_id = int(input("Enter New Client ID: "))
        except ValueError:
            print("Error: Client ID must be a number.")
            return
        if not is_valid_id(client_id):
            print("Error: Client ID must be a positive number.")
            return
        if not record_exists("get_client_by_id", "@Client_id", client_id):
            print("Error: Client with this ID does not exist.")
            return

        try:
            judge_id = int(input("Enter New Judge ID: "))
        except ValueError:
            print("Error: Judge ID must be a number.")
            return
        if not is_valid_id(judge_id):
            print("Error: Judge ID must be a positive number.")
            return
        if not record_exists("get_judge_by_id", "@Judge_id", judge_id):
            print("Error: Judge with this ID does not exist.")
            return

        case_no = input("Enter New Case No (digits only, e.g. 101): ")
        if not case_no.isdigit():
            print("Error: Case No must contain digits only.")
            return

        title = input("Enter New Case Name: ")
        if not is_not_empty(title):
            print("Error: Case Name cannot be empty.")
            return

        case_type = input("Enter New Case Type: ")
        if not is_valid_name(case_type):
            print("Error: Case Type must contain only letters and spaces.")
            return

        status = input("Enter New Case Status: ")
        if not is_valid_name(status):
            print("Error: Case Status must contain only letters and spaces.")
            return

        filed_date = input("Enter New Filed Date (YYYY-MM-DD): ")
        if not is_valid_date(filed_date):
            print("Error: Filed Date must be in YYYY-MM-DD format.")
            return

        cursor.execute(
            """
            EXEC update_case
                @Case_id=?,
                @Case_no=?,
                @Client_id=?,
                @Judge_id=?,
                @Title=?,
                @Case_type=?,
                @Status=?,
                @Filed_date=?
            """,
            (case_id, case_no, client_id, judge_id, title, case_type, status, filed_date)
        )
        connection.commit()
        print("Case updated successfully.")

    def update_case_status(self):

        try:
            case_id = int(input("Enter Case ID: "))
        except ValueError:
            print("Error: Case ID must be a number.")
            return
        if not is_valid_id(case_id):
            print("Error: Case ID must be a positive number.")
            return
        if not record_exists("get_case_by_id", "@Case_id", case_id):
            print("Error: Case with this ID does not exist.")
            return

        status = input("Enter New Status: ")
        if not is_valid_name(status):
            print("Error: Status must contain only letters and spaces.")
            return

        cursor.execute(
            "EXEC update_case_status @Case_id=?, @Status=?",
            (case_id, status)
        )
        connection.commit()
        print("Case status updated successfully.")

    def delete_case(self):

        try:
            case_id = int(input("Enter Case ID to delete: "))
        except ValueError:
            print("Error: Case ID must be a number.")
            return
        if not is_valid_id(case_id):
            print("Error: Case ID must be a positive number.")
            return
        if not record_exists("get_case_by_id", "@Case_id", case_id):
            print("Error: Case with this ID does not exist.")
            return

        cursor.execute("EXEC delete_case @Case_id=?", (case_id,))
        connection.commit()
        print("Case deleted successfully.")


class CaseLawyer:

    def assign_lawyer_to_case(self):

        try:
            assignment_id = int(input("Enter Assignment ID: "))
        except ValueError:
            print("Error: Assignment ID must be a number.")
            return
        if not is_valid_id(assignment_id):
            print("Error: Assignment ID must be a positive number.")
            return
        if record_exists("get_assignment_by_id", "@id", assignment_id):
            print("Error: Assignment with this ID already exists.")
            return

        try:
            case_id = int(input("Enter Case ID: "))
        except ValueError:
            print("Error: Case ID must be a number.")
            return
        if not is_valid_id(case_id):
            print("Error: Case ID must be a positive number.")
            return
        if not record_exists("get_case_by_id", "@Case_id", case_id):
            print("Error: Case with this ID does not exist.")
            return

        try:
            lawyer_id = int(input("Enter Lawyer ID: "))
        except ValueError:
            print("Error: Lawyer ID must be a number.")
            return
        if not is_valid_id(lawyer_id):
            print("Error: Lawyer ID must be a positive number.")
            return
        if not record_exists("get_lawyer_by_id", "@Lawyer_id", lawyer_id):
            print("Error: Lawyer with this ID does not exist.")
            return

        assigned_date = input("Enter Assigned Date (YYYY-MM-DD): ")
        if not is_valid_date(assigned_date):
            print("Error: Assigned Date must be in YYYY-MM-DD format.")
            return

        role = input("Enter Lawyer Role: ")
        if not is_valid_name(role):
            print("Error: Role must contain only letters and spaces.")
            return

        cursor.execute(
            """
            EXEC assign_lawyer_to_case
                @id=?,
                @Case_id=?,
                @Lawyer_id=?,
                @Assigned_date=?,
                @Role=?
            """,
            (assignment_id, case_id, lawyer_id, assigned_date, role)
        )
        connection.commit()
        print("Lawyer assigned to case successfully.")

    def get_all_assignments(self):

        cursor.execute("EXEC get_all_assignments")
        rows = fetch_rows()

        if len(rows) == 0:
            print("No case-lawyer assignments found.")
        else:
            for row in rows:
                print(row)

    def get_lawyers_for_case(self):

        try:
            case_id = int(input("Enter Case ID: "))
        except ValueError:
            print("Error: Case ID must be a number.")
            return
        if not is_valid_id(case_id):
            print("Error: Case ID must be a positive number.")
            return
        if not record_exists("get_case_by_id", "@Case_id", case_id):
            print("Error: Case with this ID does not exist.")
            return

        cursor.execute("EXEC get_lawyers_for_case @Case_id=?", (case_id,))
        rows = fetch_rows()

        if len(rows) == 0:
            print("Error: No lawyer assigned to this case.")
        else:
            for row in rows:
                print(row)

    def get_cases_for_lawyer(self):

        try:
            lawyer_id = int(input("Enter Lawyer ID: "))
        except ValueError:
            print("Error: Lawyer ID must be a number.")
            return
        if not is_valid_id(lawyer_id):
            print("Error: Lawyer ID must be a positive number.")
            return
        if not record_exists("get_lawyer_by_id", "@Lawyer_id", lawyer_id):
            print("Error: Lawyer with this ID does not exist.")
            return

        cursor.execute("EXEC get_cases_for_lawyer @Lawyer_id=?", (lawyer_id,))
        rows = fetch_rows()

        if len(rows) == 0:
            print("Error: No case found for this lawyer.")
        else:
            for row in rows:
                print(row)

    def update_assignment(self):

        try:
            old_case_id = int(input("Enter Existing Case ID: "))
        except ValueError:
            print("Error: Case ID must be a number.")
            return
        if not is_valid_id(old_case_id):
            print("Error: Existing Case ID must be a positive number.")
            return
        if not record_exists("get_case_by_id", "@Case_id", old_case_id):
            print("Error: Case with this ID does not exist.")
            return

        try:
            old_lawyer_id = int(input("Enter Existing Lawyer ID: "))
        except ValueError:
            print("Error: Lawyer ID must be a number.")
            return
        if not is_valid_id(old_lawyer_id):
            print("Error: Existing Lawyer ID must be a positive number.")
            return
        if not record_exists("get_lawyer_by_id", "@Lawyer_id", old_lawyer_id):
            print("Error: Lawyer with this ID does not exist.")
            return

        try:
            new_case_id = int(input("Enter New Case ID: "))
        except ValueError:
            print("Error: New Case ID must be a number.")
            return
        if not is_valid_id(new_case_id):
            print("Error: New Case ID must be a positive number.")
            return
        if not record_exists("get_case_by_id", "@Case_id", new_case_id):
            print("Error: New Case with this ID does not exist.")
            return

        try:
            new_lawyer_id = int(input("Enter New Lawyer ID: "))
        except ValueError:
            print("Error: New Lawyer ID must be a number.")
            return
        if not is_valid_id(new_lawyer_id):
            print("Error: New Lawyer ID must be a positive number.")
            return
        if not record_exists("get_lawyer_by_id", "@Lawyer_id", new_lawyer_id):
            print("Error: New Lawyer with this ID does not exist.")
            return

        cursor.execute(
            """
            EXEC update_assignment
                @Old_Case_id=?,
                @Old_Lawyer_id=?,
                @New_Case_id=?,
                @New_Lawyer_id=?
            """,
            (old_case_id, old_lawyer_id, new_case_id, new_lawyer_id)
        )
        connection.commit()
        print("Case-lawyer assignment updated successfully.")

    def delete_assignment(self):

        try:
            case_id = int(input("Enter Case ID: "))
        except ValueError:
            print("Error: Case ID must be a number.")
            return
        if not is_valid_id(case_id):
            print("Error: Case ID must be a positive number.")
            return
        if not record_exists("get_case_by_id", "@Case_id", case_id):
            print("Error: Case with this ID does not exist.")
            return

        try:
            lawyer_id = int(input("Enter Lawyer ID: "))
        except ValueError:
            print("Error: Lawyer ID must be a number.")
            return
        if not is_valid_id(lawyer_id):
            print("Error: Lawyer ID must be a positive number.")
            return
        if not record_exists("get_lawyer_by_id", "@Lawyer_id", lawyer_id):
            print("Error: Lawyer with this ID does not exist.")
            return

        cursor.execute(
            "EXEC delete_assignment @Case_id=?, @Lawyer_id=?",
            (case_id, lawyer_id)
        )
        connection.commit()
        print("Case-lawyer assignment deleted successfully.")


class TimelineEntry:

    def add_timeline_entry(self):

        try:
            entry_id = int(input("Enter Timeline ID: "))
        except ValueError:
            print("Error: Timeline ID must be a number.")
            return
        if not is_valid_id(entry_id):
            print("Error: Timeline ID must be a positive number.")
            return
        if record_exists("get_timeline_entry_by_id", "@Entry_id", entry_id):
            print("Error: Timeline entry with this ID already exists.")
            return

        try:
            case_id = int(input("Enter Case ID: "))
        except ValueError:
            print("Error: Case ID must be a number.")
            return
        if not is_valid_id(case_id):
            print("Error: Case ID must be a positive number.")
            return
        if not record_exists("get_case_by_id", "@Case_id", case_id):
            print("Error: Case with this ID does not exist.")
            return

        hearing_date = input("Enter Hearing Date (YYYY-MM-DD): ")
        if not is_valid_date(hearing_date):
            print("Error: Hearing Date must be in YYYY-MM-DD format.")
            return

        next_date = input("Enter Next Date (YYYY-MM-DD): ")
        if not is_valid_date(next_date):
            print("Error: Next Date must be in YYYY-MM-DD format.")
            return

        proceeding_type = input("Enter Proceeding Type: ")
        if not is_valid_name(proceeding_type):
            print("Error: Proceeding Type must contain only letters and spaces.")
            return

        outcome = input("Enter Outcome: ")
        if not is_valid_name(outcome):
            print("Error: Outcome must contain only letters and spaces.")
            return

        note = input("Enter Note: ")

        cursor.execute(
            """
            EXEC add_timeline_entry
                @Entry_id=?,
                @Case_id=?,
                @Hearing_date=?,
                @Next_date=?,
                @Proceeding_type=?,
                @Outcome=?,
                @Note=?
            """,
            (entry_id, case_id, hearing_date, next_date, proceeding_type, outcome, note)
        )
        connection.commit()
        print("Timeline entry added successfully.")

    def get_all_timeline_entries(self):

        cursor.execute("EXEC get_all_timeline_entries")
        rows = fetch_rows()

        if len(rows) == 0:
            print("No timeline entries found.")
        else:
            for row in rows:
                print(row)

    def get_timeline_for_case(self):

        try:
            case_id = int(input("Enter Case ID: "))
        except ValueError:
            print("Error: Case ID must be a number.")
            return
        if not is_valid_id(case_id):
            print("Error: Case ID must be a positive number.")
            return
        if not record_exists("get_case_by_id", "@Case_id", case_id):
            print("Error: Case with this ID does not exist.")
            return

        cursor.execute("EXEC get_timeline_for_case @Case_id=?", (case_id,))
        rows = fetch_rows()

        if len(rows) == 0:
            print("Error: No timeline found for this case.")
        else:
            for row in rows:
                print(row)

    def update_timeline_entry(self):

        try:
            entry_id = int(input("Enter Timeline ID to update: "))
        except ValueError:
            print("Error: Timeline ID must be a number.")
            return
        if not is_valid_id(entry_id):
            print("Error: Timeline ID must be a positive number.")
            return
        if not record_exists("get_timeline_entry_by_id", "@Entry_id", entry_id):
            print("Error: Timeline entry with this ID does not exist.")
            return

        try:
            case_id = int(input("Enter New Case ID: "))
        except ValueError:
            print("Error: Case ID must be a number.")
            return
        if not is_valid_id(case_id):
            print("Error: Case ID must be a positive number.")
            return
        if not record_exists("get_case_by_id", "@Case_id", case_id):
            print("Error: Case with this ID does not exist.")
            return

        hearing_date = input("Enter New Hearing Date (YYYY-MM-DD): ")
        if not is_valid_date(hearing_date):
            print("Error: Hearing Date must be in YYYY-MM-DD format.")
            return

        next_date = input("Enter New Next Date (YYYY-MM-DD): ")
        if not is_valid_date(next_date):
            print("Error: Next Date must be in YYYY-MM-DD format.")
            return

        proceeding_type = input("Enter New Proceeding Type: ")
        if not is_valid_name(proceeding_type):
            print("Error: Proceeding Type must contain only letters and spaces.")
            return

        outcome = input("Enter New Outcome: ")
        if not is_valid_name(outcome):
            print("Error: Outcome must contain only letters and spaces.")
            return

        note = input("Enter New Note: ")

        cursor.execute(
            """
            EXEC update_timeline_entry
                @Entry_id=?,
                @Case_id=?,
                @Hearing_date=?,
                @Next_date=?,
                @Proceeding_type=?,
                @Outcome=?,
                @Note=?
            """,
            (entry_id, case_id, hearing_date, next_date, proceeding_type, outcome, note)
        )
        connection.commit()
        print("Timeline entry updated successfully.")

    def delete_timeline_entry(self):

        try:
            entry_id = int(input("Enter Timeline ID to delete: "))
        except ValueError:
            print("Error: Timeline ID must be a number.")
            return
        if not is_valid_id(entry_id):
            print("Error: Timeline ID must be a positive number.")
            return
        if not record_exists("get_timeline_entry_by_id", "@Entry_id", entry_id):
            print("Error: Timeline entry with this ID does not exist.")
            return

        cursor.execute("EXEC delete_timeline_entry @Entry_id=?", (entry_id,))
        connection.commit()
        print("Timeline entry deleted successfully.")


class Journal:

    def add_journal_entry(self):

        try:
            journal_id = int(input("Enter Journal ID: "))
        except ValueError:
            print("Error: Journal ID must be a number.")
            return
        if not is_valid_id(journal_id):
            print("Error: Journal ID must be a positive number.")
            return
        if record_exists("get_journal_by_id", "@Journal_id", journal_id):
            print("Error: Journal entry with this ID already exists.")
            return

        try:
            case_id = int(input("Enter Case ID: "))
        except ValueError:
            print("Error: Case ID must be a number.")
            return
        if not is_valid_id(case_id):
            print("Error: Case ID must be a positive number.")
            return
        if not record_exists("get_case_by_id", "@Case_id", case_id):
            print("Error: Case with this ID does not exist.")
            return

        try:
            lawyer_id = int(input("Enter Lawyer ID: "))
        except ValueError:
            print("Error: Lawyer ID must be a number.")
            return
        if not is_valid_id(lawyer_id):
            print("Error: Lawyer ID must be a positive number.")
            return
        if not record_exists("get_lawyer_by_id", "@Lawyer_id", lawyer_id):
            print("Error: Lawyer with this ID does not exist.")
            return
        if not lawyer_assigned_to_case(case_id, lawyer_id):
            print("Error: This lawyer is not assigned to this case.")
            return

        entry_date = input("Enter Entry Date (YYYY-MM-DD): ")
        if not is_valid_date(entry_date):
            print("Error: Entry Date must be in YYYY-MM-DD format.")
            return

        entry_type = input("Enter Entry Type: ")
        if not is_valid_name(entry_type):
            print("Error: Entry Type must contain only letters and spaces.")
            return

        content = input("Enter Content: ")
        if not is_not_empty(content):
            print("Error: Content cannot be empty.")
            return

        cursor.execute(
            """
            EXEC add_journal_entry
                @Journal_id=?,
                @Case_id=?,
                @Lawyer_id=?,
                @Entry_date=?,
                @Entry_type=?,
                @Content=?
            """,
            (journal_id, case_id, lawyer_id, entry_date, entry_type, content)
        )
        connection.commit()
        print("Journal entry added successfully.")

    def get_all_journals(self):

        cursor.execute("EXEC get_all_journals")
        rows = fetch_rows()

        if len(rows) == 0:
            print("No journal entries found.")
        else:
            for row in rows:
                print(row)

    def get_journal_for_case(self):

        try:
            case_id = int(input("Enter Case ID: "))
        except ValueError:
            print("Error: Case ID must be a number.")
            return
        if not is_valid_id(case_id):
            print("Error: Case ID must be a positive number.")
            return
        if not record_exists("get_case_by_id", "@Case_id", case_id):
            print("Error: Case with this ID does not exist.")
            return

        cursor.execute("EXEC get_journal_for_case @Case_id=?", (case_id,))
        rows = fetch_rows()

        if len(rows) == 0:
            print("Error: No journal found for this case.")
        else:
            for row in rows:
                print(row)

    def update_journal_entry(self):

        try:
            journal_id = int(input("Enter Journal ID to update: "))
        except ValueError:
            print("Error: Journal ID must be a number.")
            return
        if not is_valid_id(journal_id):
            print("Error: Journal ID must be a positive number.")
            return
        if not record_exists("get_journal_by_id", "@Journal_id", journal_id):
            print("Error: Journal entry with this ID does not exist.")
            return

        try:
            case_id = int(input("Enter New Case ID: "))
        except ValueError:
            print("Error: Case ID must be a number.")
            return
        if not is_valid_id(case_id):
            print("Error: Case ID must be a positive number.")
            return
        if not record_exists("get_case_by_id", "@Case_id", case_id):
            print("Error: Case with this ID does not exist.")
            return

        try:
            lawyer_id = int(input("Enter New Lawyer ID: "))
        except ValueError:
            print("Error: Lawyer ID must be a number.")
            return
        if not is_valid_id(lawyer_id):
            print("Error: Lawyer ID must be a positive number.")
            return
        if not record_exists("get_lawyer_by_id", "@Lawyer_id", lawyer_id):
            print("Error: Lawyer with this ID does not exist.")
            return
        if not lawyer_assigned_to_case(case_id, lawyer_id):
            print("Error: This lawyer is not assigned to this case.")
            return

        entry_date = input("Enter New Entry Date (YYYY-MM-DD): ")
        if not is_valid_date(entry_date):
            print("Error: Entry Date must be in YYYY-MM-DD format.")
            return

        entry_type = input("Enter New Entry Type: ")
        if not is_valid_name(entry_type):
            print("Error: Entry Type must contain only letters and spaces.")
            return

        content = input("Enter New Content: ")
        if not is_not_empty(content):
            print("Error: Content cannot be empty.")
            return

        cursor.execute(
            """
            EXEC update_journal_entry
                @Journal_id=?,
                @Case_id=?,
                @Lawyer_id=?,
                @Entry_date=?,
                @Entry_type=?,
                @Content=?
            """,
            (journal_id, case_id, lawyer_id, entry_date, entry_type, content)
        )
        connection.commit()
        print("Journal entry updated successfully.")

    def delete_journal_entry(self):

        try:
            journal_id = int(input("Enter Journal ID to delete: "))
        except ValueError:
            print("Error: Journal ID must be a number.")
            return
        if not is_valid_id(journal_id):
            print("Error: Journal ID must be a positive number.")
            return
        if not record_exists("get_journal_by_id", "@Journal_id", journal_id):
            print("Error: Journal entry with this ID does not exist.")
            return

        cursor.execute("EXEC delete_journal_entry @Journal_id=?", (journal_id,))
        connection.commit()
        print("Journal entry deleted successfully.")


class Evidence:

    def add_evidence(self):

        try:
            evidence_id = int(input("Enter Evidence ID: "))
        except ValueError:
            print("Error: Evidence ID must be a number.")
            return
        if not is_valid_id(evidence_id):
            print("Error: Evidence ID must be a positive number.")
            return
        if record_exists("get_evidence_by_id", "@Evidence_id", evidence_id):
            print("Error: Evidence with this ID already exists.")
            return

        try:
            case_id = int(input("Enter Case ID: "))
        except ValueError:
            print("Error: Case ID must be a number.")
            return
        if not is_valid_id(case_id):
            print("Error: Case ID must be a positive number.")
            return
        if not record_exists("get_case_by_id", "@Case_id", case_id):
            print("Error: Case with this ID does not exist.")
            return

        title = input("Enter Evidence Title: ")
        if not is_not_empty(title):
            print("Error: Evidence Title cannot be empty.")
            return
        if record_exists("get_evidence_by_title", "@Title", title):
            print("Error: Evidence with this title already exists.")
            return

        evidence_type = input("Enter Evidence Type: ")
        if not is_valid_name(evidence_type):
            print("Error: Evidence Type must contain only letters and spaces.")
            return

        description = input("Enter Description: ")

        submitted_date = input("Enter Submitted Date (YYYY-MM-DD): ")
        if not is_valid_date(submitted_date):
            print("Error: Submitted Date must be in YYYY-MM-DD format.")
            return

        file_path = input("Enter File Path: ")

        cursor.execute(
            """
            EXEC add_evidence
                @Evidence_id=?,
                @Case_id=?,
                @Title=?,
                @Evidence_type=?,
                @Description=?,
                @Submitted_date=?,
                @File_path=?
            """,
            (evidence_id, case_id, title, evidence_type, description, submitted_date, file_path)
        )
        connection.commit()
        print("Evidence added successfully.")

    def get_all_evidence(self):

        cursor.execute("EXEC get_all_evidence")
        rows = fetch_rows()

        if len(rows) == 0:
            print("No evidence found.")
        else:
            for row in rows:
                print(row)

    def get_evidence_for_case(self):

        try:
            case_id = int(input("Enter Case ID: "))
        except ValueError:
            print("Error: Case ID must be a number.")
            return
        if not is_valid_id(case_id):
            print("Error: Case ID must be a positive number.")
            return
        if not record_exists("get_case_by_id", "@Case_id", case_id):
            print("Error: Case with this ID does not exist.")
            return

        cursor.execute("EXEC get_evidence_for_case @Case_id=?", (case_id,))
        rows = fetch_rows()

        if len(rows) == 0:
            print("Error: No evidence found for this case.")
        else:
            for row in rows:
                print(row)

    def update_evidence(self):

        try:
            evidence_id = int(input("Enter Evidence ID to update: "))
        except ValueError:
            print("Error: Evidence ID must be a number.")
            return
        if not is_valid_id(evidence_id):
            print("Error: Evidence ID must be a positive number.")
            return
        if not record_exists("get_evidence_by_id", "@Evidence_id", evidence_id):
            print("Error: Evidence with this ID does not exist.")
            return

        try:
            case_id = int(input("Enter New Case ID: "))
        except ValueError:
            print("Error: Case ID must be a number.")
            return
        if not is_valid_id(case_id):
            print("Error: Case ID must be a positive number.")
            return
        if not record_exists("get_case_by_id", "@Case_id", case_id):
            print("Error: Case with this ID does not exist.")
            return

        title = input("Enter New Evidence Title: ")
        if not is_not_empty(title):
            print("Error: Evidence Title cannot be empty.")
            return

        evidence_type = input("Enter New Evidence Type: ")
        if not is_valid_name(evidence_type):
            print("Error: Evidence Type must contain only letters and spaces.")
            return

        description = input("Enter New Description: ")

        submitted_date = input("Enter New Submitted Date (YYYY-MM-DD): ")
        if not is_valid_date(submitted_date):
            print("Error: Submitted Date must be in YYYY-MM-DD format.")
            return

        file_path = input("Enter New File Path: ")

        cursor.execute(
            """
            EXEC update_evidence
                @Evidence_id=?,
                @Case_id=?,
                @Title=?,
                @Evidence_type=?,
                @Description=?,
                @Submitted_date=?,
                @File_path=?
            """,
            (evidence_id, case_id, title, evidence_type, description, submitted_date, file_path)
        )
        connection.commit()
        print("Evidence updated successfully.")

    def delete_evidence(self):

        try:
            evidence_id = int(input("Enter Evidence ID to delete: "))
        except ValueError:
            print("Error: Evidence ID must be a number.")
            return
        if not is_valid_id(evidence_id):
            print("Error: Evidence ID must be a positive number.")
            return
        if not record_exists("get_evidence_by_id", "@Evidence_id", evidence_id):
            print("Error: Evidence with this ID does not exist.")
            return

        cursor.execute("EXEC delete_evidence @Evidence_id=?", (evidence_id,))
        connection.commit()
        print("Evidence deleted successfully.")


class Payment:

    def add_payment(self):

        try:
            payment_id = int(input("Enter Payment ID: "))
        except ValueError:
            print("Error: Payment ID must be a number.")
            return
        if not is_valid_id(payment_id):
            print("Error: Payment ID must be a positive number.")
            return
        if record_exists("get_payment_by_id", "@Payment_id", payment_id):
            print("Error: Payment with this ID already exists.")
            return

        try:
            case_id = int(input("Enter Case ID: "))
        except ValueError:
            print("Error: Case ID must be a number.")
            return
        if not is_valid_id(case_id):
            print("Error: Case ID must be a positive number.")
            return
        if not record_exists("get_case_by_id", "@Case_id", case_id):
            print("Error: Case with this ID does not exist.")
            return

        try:
            lawyer_id = int(input("Enter Lawyer ID: "))
        except ValueError:
            print("Error: Lawyer ID must be a number.")
            return
        if not is_valid_id(lawyer_id):
            print("Error: Lawyer ID must be a positive number.")
            return
        if not record_exists("get_lawyer_by_id", "@Lawyer_id", lawyer_id):
            print("Error: Lawyer with this ID does not exist.")
            return

        try:
            client_id = int(input("Enter Client ID: "))
        except ValueError:
            print("Error: Client ID must be a number.")
            return
        if not is_valid_id(client_id):
            print("Error: Client ID must be a positive number.")
            return
        if not record_exists("get_client_by_id", "@Client_id", client_id):
            print("Error: Client with this ID does not exist.")
            return
        if not lawyer_assigned_to_case(case_id, lawyer_id):
            print("Error: This lawyer is not assigned to this case.")
            return
        if not client_belongs_to_case(case_id, client_id):
            print("Error: This client is not associated with this case.")
            return

        try:
            amount = float(input("Enter Amount: "))
        except ValueError:
            print("Error: Amount must be a number.")
            return
        if not is_valid_amount(amount):
            print("Error: Amount must be greater than 0.")
            return

        payment_date = input("Enter Payment Date (YYYY-MM-DD): ")
        if not is_valid_date(payment_date):
            print("Error: Payment Date must be in YYYY-MM-DD format.")
            return

        status = input("Enter Payment Status: ")
        if not is_valid_name(status):
            print("Error: Payment Status must contain only letters and spaces.")
            return

        description = input("Enter Description: ")

        cursor.execute(
            """
            EXEC add_payment
                @Payment_id=?,
                @Case_id=?,
                @Lawyer_id=?,
                @Client_id=?,
                @Amount=?,
                @Payment_date=?,
                @Status=?,
                @Description=?
            """,
            (payment_id, case_id, lawyer_id, client_id, amount, payment_date, status, description)
        )
        connection.commit()
        print("Payment added successfully.")

    def get_all_payments(self):

        cursor.execute("EXEC get_all_payments")
        rows = fetch_rows()

        if len(rows) == 0:
            print("No payments found.")
        else:
            for row in rows:
                print(row)

    def get_payments_for_case(self):

        try:
            case_id = int(input("Enter Case ID: "))
        except ValueError:
            print("Error: Case ID must be a number.")
            return
        if not is_valid_id(case_id):
            print("Error: Case ID must be a positive number.")
            return
        if not record_exists("get_case_by_id", "@Case_id", case_id):
            print("Error: Case with this ID does not exist.")
            return

        cursor.execute("EXEC get_payments_for_case @Case_id=?", (case_id,))
        rows = fetch_rows()

        if len(rows) == 0:
            print("Error: No payment found for this case.")
        else:
            for row in rows:
                print(row)

    def update_payment(self):

        try:
            payment_id = int(input("Enter Payment ID to update: "))
        except ValueError:
            print("Error: Payment ID must be a number.")
            return
        if not is_valid_id(payment_id):
            print("Error: Payment ID must be a positive number.")
            return
        if not record_exists("get_payment_by_id", "@Payment_id", payment_id):
            print("Error: Payment with this ID does not exist.")
            return

        try:
            case_id = int(input("Enter New Case ID: "))
        except ValueError:
            print("Error: Case ID must be a number.")
            return
        if not is_valid_id(case_id):
            print("Error: Case ID must be a positive number.")
            return
        if not record_exists("get_case_by_id", "@Case_id", case_id):
            print("Error: Case with this ID does not exist.")
            return

        try:
            lawyer_id = int(input("Enter New Lawyer ID: "))
        except ValueError:
            print("Error: Lawyer ID must be a number.")
            return
        if not is_valid_id(lawyer_id):
            print("Error: Lawyer ID must be a positive number.")
            return
        if not record_exists("get_lawyer_by_id", "@Lawyer_id", lawyer_id):
            print("Error: Lawyer with this ID does not exist.")
            return

        try:
            client_id = int(input("Enter New Client ID: "))
        except ValueError:
            print("Error: Client ID must be a number.")
            return
        if not is_valid_id(client_id):
            print("Error: Client ID must be a positive number.")
            return
        if not record_exists("get_client_by_id", "@Client_id", client_id):
            print("Error: Client with this ID does not exist.")
            return
        if not lawyer_assigned_to_case(case_id, lawyer_id):
            print("Error: This lawyer is not assigned to this case.")
            return
        if not client_belongs_to_case(case_id, client_id):
            print("Error: This client is not associated with this case.")
            return

        try:
            amount = float(input("Enter New Amount: "))
        except ValueError:
            print("Error: Amount must be a number.")
            return
        if not is_valid_amount(amount):
            print("Error: Amount must be greater than 0.")
            return

        payment_date = input("Enter New Payment Date (YYYY-MM-DD): ")
        if not is_valid_date(payment_date):
            print("Error: Payment Date must be in YYYY-MM-DD format.")
            return

        status = input("Enter New Payment Status: ")
        if not is_valid_name(status):
            print("Error: Payment Status must contain only letters and spaces.")
            return

        description = input("Enter New Description: ")

        cursor.execute(
            """
            EXEC update_payment
                @Payment_id=?,
                @Case_id=?,
                @Lawyer_id=?,
                @Client_id=?,
                @Amount=?,
                @Payment_date=?,
                @Status=?,
                @Description=?
            """,
            (payment_id, case_id, lawyer_id, client_id, amount, payment_date, status, description)
        )
        connection.commit()
        print("Payment updated successfully.")

    def update_payment_status(self):

        try:
            payment_id = int(input("Enter Payment ID: "))
        except ValueError:
            print("Error: Payment ID must be a number.")
            return
        if not is_valid_id(payment_id):
            print("Error: Payment ID must be a positive number.")
            return
        if not record_exists("get_payment_by_id", "@Payment_id", payment_id):
            print("Error: Payment with this ID does not exist.")
            return

        status = input("Enter New Payment Status: ")
        if not is_valid_name(status):
            print("Error: Payment Status must contain only letters and spaces.")
            return

        cursor.execute(
            "EXEC update_payment_status @Payment_id=?, @Status=?",
            (payment_id, status)
        )
        connection.commit()
        print("Payment status updated successfully.")

    def delete_payment(self):

        try:
            payment_id = int(input("Enter Payment ID to delete: "))
        except ValueError:
            print("Error: Payment ID must be a number.")
            return
        if not is_valid_id(payment_id):
            print("Error: Payment ID must be a positive number.")
            return
        if not record_exists("get_payment_by_id", "@Payment_id", payment_id):
            print("Error: Payment with this ID does not exist.")
            return

        cursor.execute("EXEC delete_payment @Payment_id=?", (payment_id,))
        connection.commit()
        print("Payment deleted successfully.")

    def get_total_paid_amount(self):

        try:
            case_id = int(input("Enter Case ID: "))
        except ValueError:
            print("Error: Case ID must be a number.")
            return
        if not is_valid_id(case_id):
            print("Error: Case ID must be a positive number.")
            return
        if not record_exists("get_case_by_id", "@Case_id", case_id):
            print("Error: Case with this ID does not exist.")
            return

        cursor.execute("EXEC get_total_paid_amount @Case_id=?", (case_id,))
        rows = fetch_rows()

        for row in rows:
            print("Total Paid Amount:", row[0])


# Menu Functions 

def judge_menu():
    judge = Judge()
    while True:
        print("\n~~~ Judge Menu ~~~")
        print("1. Add Judge")
        print("2. View All Judges")
        print("3. Search Judge by ID")
        print("4. Update Judge")
        print("5. Delete Judge")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            judge.add_judge()
        elif choice == "2":
            judge.get_all_judges()
        elif choice == "3":
            judge.get_judge_by_id()
        elif choice == "4":
            judge.update_judge()
        elif choice == "5":
            judge.delete_judge()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


def client_menu():
    client = Client()
    while True:
        print("\n~~~ Client Menu ~~~")
        print("1. Add Client")
        print("2. View All Clients")
        print("3. Search Client by ID")
        print("4. Update Client")
        print("5. Delete Client")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            client.add_client()
        elif choice == "2":
            client.get_all_clients()
        elif choice == "3":
            client.get_client_by_id()
        elif choice == "4":
            client.update_client()
        elif choice == "5":
            client.delete_client()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


def lawyer_menu():
    lawyer = Lawyer()
    while True:
        print("\n~~~ Lawyer Menu ~~~")
        print("1. Add Lawyer")
        print("2. View All Lawyers")
        print("3. Search Lawyer by ID")
        print("4. Update Lawyer")
        print("5. Delete Lawyer")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            lawyer.add_lawyer()
        elif choice == "2":
            lawyer.get_all_lawyers()
        elif choice == "3":
            lawyer.get_lawyer_by_id()
        elif choice == "4":
            lawyer.update_lawyer()
        elif choice == "5":
            lawyer.delete_lawyer()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


def case_menu():
    case = Case()
    while True:
        print("\n~~~ Case Menu ~~~")
        print("1. Add Case")
        print("2. View All Cases")
        print("3. Search Case by ID")
        print("4. Search Cases by Client")
        print("5. Search Cases by Status")
        print("6. Update Case")
        print("7. Update Case Status")
        print("8. Delete Case")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            case.add_case()
        elif choice == "2":
            case.get_all_cases()
        elif choice == "3":
            case.get_case_by_id()
        elif choice == "4":
            case.get_cases_by_client()
        elif choice == "5":
            case.get_cases_by_status()
        elif choice == "6":
            case.update_case()
        elif choice == "7":
            case.update_case_status()
        elif choice == "8":
            case.delete_case()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


def case_lawyer_menu():
    case_lawyer = CaseLawyer()
    while True:
        print("\n~~~ Case-Lawyer Assignment Menu ~~~")
        print("1. Assign Lawyer to Case")
        print("2. View All Assignments")
        print("3. View Lawyers for a Case")
        print("4. View Cases for a Lawyer")
        print("5. Update Assignment")
        print("6. Delete Assignment")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            case_lawyer.assign_lawyer_to_case()
        elif choice == "2":
            case_lawyer.get_all_assignments()
        elif choice == "3":
            case_lawyer.get_lawyers_for_case()
        elif choice == "4":
            case_lawyer.get_cases_for_lawyer()
        elif choice == "5":
            case_lawyer.update_assignment()
        elif choice == "6":
            case_lawyer.delete_assignment()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


def timeline_menu():
    timeline = TimelineEntry()
    while True:
        print("\n~~~ Timeline Entry Menu ~~~")
        print("1. Add Timeline Entry")
        print("2. View All Timeline Entries")
        print("3. View Timeline for a Case")
        print("4. Update Timeline Entry")
        print("5. Delete Timeline Entry")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            timeline.add_timeline_entry()
        elif choice == "2":
            timeline.get_all_timeline_entries()
        elif choice == "3":
            timeline.get_timeline_for_case()
        elif choice == "4":
            timeline.update_timeline_entry()
        elif choice == "5":
            timeline.delete_timeline_entry()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


def journal_menu():
    journal = Journal()
    while True:
        print("\n~~~ Journal Menu ~~~")
        print("1. Add Journal Entry")
        print("2. View All Journal Entries")
        print("3. View Journal for a Case")
        print("4. Update Journal Entry")
        print("5. Delete Journal Entry")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            journal.add_journal_entry()
        elif choice == "2":
            journal.get_all_journals()
        elif choice == "3":
            journal.get_journal_for_case()
        elif choice == "4":
            journal.update_journal_entry()
        elif choice == "5":
            journal.delete_journal_entry()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


def evidence_menu():
    evidence = Evidence()
    while True:
        print("\n~~~ Evidence Menu ~~~")
        print("1. Add Evidence")
        print("2. View All Evidence")
        print("3. View Evidence for a Case")
        print("4. Update Evidence")
        print("5. Delete Evidence")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            evidence.add_evidence()
        elif choice == "2":
            evidence.get_all_evidence()
        elif choice == "3":
            evidence.get_evidence_for_case()
        elif choice == "4":
            evidence.update_evidence()
        elif choice == "5":
            evidence.delete_evidence()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


def payment_menu():
    payment = Payment()
    while True:
        print("\n~~~ Payment Menu ~~~")
        print("1. Add Payment")
        print("2. View All Payments")
        print("3. View Payments for a Case")
        print("4. Update Payment")
        print("5. Update Payment Status")
        print("6. Delete Payment")
        print("7. Get Total Paid Amount for a Case")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == "1":
            payment.add_payment()
        elif choice == "2":
            payment.get_all_payments()
        elif choice == "3":
            payment.get_payments_for_case()
        elif choice == "4":
            payment.update_payment()
        elif choice == "5":
            payment.update_payment_status()
        elif choice == "6":
            payment.delete_payment()
        elif choice == "7":
            payment.get_total_paid_amount()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")


def main_menu():
    while True:
        print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("  Law Firm Management System")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("1. Judge")
        print("2. Client")
        print("3. Lawyer")
        print("4. Case")
        print("5. Case-Lawyer Assignment")
        print("6. Timeline Entry")
        print("7. Journal")
        print("8. Evidence")
        print("9. Payment")
        print("0. Exit")
        print("______________________________")
        choice = input("Enter your choice: ")

        if choice == "1":
            judge_menu()
        elif choice == "2":
            client_menu()
        elif choice == "3":
            lawyer_menu()
        elif choice == "4":
            case_menu()
        elif choice == "5":
            case_lawyer_menu()
        elif choice == "6":
            timeline_menu()
        elif choice == "7":
            journal_menu()
        elif choice == "8":
            evidence_menu()
        elif choice == "9":
            payment_menu()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


main_menu()
