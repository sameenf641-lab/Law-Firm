import streamlit as st
import pyodbc

st.set_page_config(
    page_title=".~Law Firm Management System~.",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Column headers 
COLS = {
    "Judge":      ["Judge ID", "Name", "Court Name", "Specialization", "Contact Info"],
    "Client":     ["Client ID", "Name", "CNIC", "Phone No", "Email", "Street", "City"],
    "Lawyer":     ["Lawyer ID", "Name", "Email", "Bar Number", "Specialization", "Phone No", "Hourly Rate"],
    "Case":       ["Case ID", "Case No", "Title", "Type", "Status", "Filed Date", "Client ID", "Judge ID"],
    "CaseLawyer": ["ID", "Case ID", "Lawyer ID", "Assigned Date", "Role"],
    "Timeline":   ["Entry ID", "Case ID", "Hearing Date", "Next Date", "Proceeding Type", "Outcome", "Note"],
    "Journal":    ["Journal ID", "Case ID", "Lawyer ID", "Entry Date", "Entry Type", "Content"],
    "Evidence":   ["Evidence ID", "Case ID", "Title", "Type", "Description", "Submitted Date", "File Path"],
    "Payment":    ["Payment ID", "Case ID", "Lawyer ID", "Client ID", "Amount", "Payment Date", "Status", "Description"],
}

# Stored Procedures 
PROCEDURES = [
    """CREATE OR ALTER PROCEDURE add_judge
        @Judge_id INT, @Name VARCHAR(100), @Court_name VARCHAR(100),
        @Specialization VARCHAR(100), @Contact_info VARCHAR(200)
    AS BEGIN
        IF EXISTS (SELECT 1 FROM Judge WHERE Judge_id=@Judge_id)
            BEGIN PRINT 'Error: ID exists.'; RETURN; END
        IF EXISTS (SELECT 1 FROM Judge WHERE Name=@Name)
            BEGIN PRINT 'Error: Name exists.'; RETURN; END
        INSERT INTO Judge VALUES (@Judge_id,@Name,@Court_name,@Specialization,@Contact_info);
    END""",
    "CREATE OR ALTER PROCEDURE get_all_judges AS BEGIN SELECT * FROM Judge; END",
    "CREATE OR ALTER PROCEDURE get_judge_by_id @Judge_id INT AS BEGIN SELECT * FROM Judge WHERE Judge_id=@Judge_id; END",
    "CREATE OR ALTER PROCEDURE get_judge_by_name @Name VARCHAR(100) AS BEGIN SELECT * FROM Judge WHERE Name=@Name; END",
    """CREATE OR ALTER PROCEDURE update_judge
        @Judge_id INT, @Name VARCHAR(100), @Court_name VARCHAR(100),
        @Specialization VARCHAR(100), @Contact_info VARCHAR(200)
    AS BEGIN
        IF EXISTS (SELECT 1 FROM Judge WHERE Judge_id=@Judge_id)
            UPDATE Judge SET Name=@Name,Court_name=@Court_name,Specialization=@Specialization,Contact_info=@Contact_info WHERE Judge_id=@Judge_id;
        ELSE PRINT 'Error: Not found.';
    END""",
    "CREATE OR ALTER PROCEDURE delete_judge @Judge_id INT AS BEGIN IF EXISTS (SELECT 1 FROM Judge WHERE Judge_id=@Judge_id) DELETE FROM Judge WHERE Judge_id=@Judge_id; ELSE PRINT 'Error: Not found.'; END",

    """CREATE OR ALTER PROCEDURE add_client
        @Client_id INT, @Name VARCHAR(100), @CNIC VARCHAR(20),
        @Phone_no VARCHAR(20), @Email VARCHAR(100), @Street VARCHAR(100), @City VARCHAR(100)
    AS BEGIN
        IF EXISTS (SELECT 1 FROM Client WHERE Client_id=@Client_id)
            BEGIN PRINT 'Error: ID exists.'; RETURN; END
        INSERT INTO Client VALUES (@Client_id,@Name,@CNIC,@Phone_no,@Email,@Street,@City);
    END""",
    "CREATE OR ALTER PROCEDURE get_all_clients AS BEGIN SELECT * FROM Client; END",
    "CREATE OR ALTER PROCEDURE get_client_by_id @Client_id INT AS BEGIN SELECT * FROM Client WHERE Client_id=@Client_id; END",
    "CREATE OR ALTER PROCEDURE get_client_by_name @Name VARCHAR(100) AS BEGIN SELECT * FROM Client WHERE Name=@Name; END",
    """CREATE OR ALTER PROCEDURE update_client
        @Client_id INT, @Name VARCHAR(100), @CNIC VARCHAR(20),
        @Phone_no VARCHAR(20), @Email VARCHAR(100), @Street VARCHAR(100), @City VARCHAR(100)
    AS BEGIN
        IF EXISTS (SELECT 1 FROM Client WHERE Client_id=@Client_id)
            UPDATE Client SET Name=@Name,CNIC=@CNIC,Phone_no=@Phone_no,Email=@Email,Street=@Street,City=@City WHERE Client_id=@Client_id;
        ELSE PRINT 'Error: Not found.';
    END""",
    "CREATE OR ALTER PROCEDURE delete_client @Client_id INT AS BEGIN IF EXISTS (SELECT 1 FROM Client WHERE Client_id=@Client_id) DELETE FROM Client WHERE Client_id=@Client_id; ELSE PRINT 'Error: Not found.'; END",

    """CREATE OR ALTER PROCEDURE add_lawyer
        @Lawyer_id INT, @Name VARCHAR(100), @Email VARCHAR(100), @Bar_number VARCHAR(50),
        @Specialization VARCHAR(100), @Phone_no VARCHAR(20), @Hourly_rate DECIMAL(10,2)
    AS BEGIN
        IF EXISTS (SELECT 1 FROM Lawyer WHERE Lawyer_id=@Lawyer_id)
            BEGIN PRINT 'Error: ID exists.'; RETURN; END
        INSERT INTO Lawyer VALUES (@Lawyer_id,@Name,@Email,@Bar_number,@Specialization,@Phone_no,@Hourly_rate);
    END""",
    "CREATE OR ALTER PROCEDURE get_all_lawyers AS BEGIN SELECT * FROM Lawyer; END",
    "CREATE OR ALTER PROCEDURE get_lawyer_by_id @Lawyer_id INT AS BEGIN SELECT * FROM Lawyer WHERE Lawyer_id=@Lawyer_id; END",
    "CREATE OR ALTER PROCEDURE get_lawyer_by_name @Name VARCHAR(100) AS BEGIN SELECT * FROM Lawyer WHERE Name=@Name; END",
    """CREATE OR ALTER PROCEDURE update_lawyer
        @Lawyer_id INT, @Name VARCHAR(100), @Email VARCHAR(100), @Bar_number VARCHAR(50),
        @Specialization VARCHAR(100), @Phone_no VARCHAR(20), @Hourly_rate DECIMAL(10,2)
    AS BEGIN
        IF EXISTS (SELECT 1 FROM Lawyer WHERE Lawyer_id=@Lawyer_id)
            UPDATE Lawyer SET Name=@Name,Email=@Email,Bar_number=@Bar_number,Specialization=@Specialization,Phone_no=@Phone_no,Hourly_rate=@Hourly_rate WHERE Lawyer_id=@Lawyer_id;
        ELSE PRINT 'Error: Not found.';
    END""",
    "CREATE OR ALTER PROCEDURE delete_lawyer @Lawyer_id INT AS BEGIN IF EXISTS (SELECT 1 FROM Lawyer WHERE Lawyer_id=@Lawyer_id) DELETE FROM Lawyer WHERE Lawyer_id=@Lawyer_id; ELSE PRINT 'Error: Not found.'; END",

    """CREATE OR ALTER PROCEDURE add_case
        @Case_id INT, @Case_no VARCHAR(50), @Client_id INT, @Judge_id INT,
        @Title VARCHAR(150), @Case_type VARCHAR(100), @Status VARCHAR(50), @Filed_date DATE
    AS BEGIN
        IF EXISTS (SELECT 1 FROM [Case] WHERE Case_id=@Case_id)
            BEGIN PRINT 'Error: ID exists.'; RETURN; END
        INSERT INTO [Case] (Case_id,Case_no,Title,Case_type,Status,Filed_date,Client_id,Judge_id)
        VALUES (@Case_id,@Case_no,@Title,@Case_type,@Status,@Filed_date,@Client_id,@Judge_id);
    END""",
    "CREATE OR ALTER PROCEDURE get_all_cases AS BEGIN SELECT * FROM [Case]; END",
    "CREATE OR ALTER PROCEDURE get_case_by_id @Case_id INT AS BEGIN SELECT * FROM [Case] WHERE Case_id=@Case_id; END",
    "CREATE OR ALTER PROCEDURE get_cases_by_client @Client_id INT AS BEGIN SELECT * FROM [Case] WHERE Client_id=@Client_id; END",
    "CREATE OR ALTER PROCEDURE get_cases_by_status @Status VARCHAR(50) AS BEGIN SELECT * FROM [Case] WHERE Status=@Status; END",
    "CREATE OR ALTER PROCEDURE get_case_by_title @Title VARCHAR(150) AS BEGIN SELECT * FROM [Case] WHERE Title=@Title; END",
    """CREATE OR ALTER PROCEDURE update_case
        @Case_id INT, @Case_no VARCHAR(50), @Client_id INT, @Judge_id INT,
        @Title VARCHAR(150), @Case_type VARCHAR(100), @Status VARCHAR(50), @Filed_date DATE
    AS BEGIN
        IF EXISTS (SELECT 1 FROM [Case] WHERE Case_id=@Case_id)
            UPDATE [Case] SET Case_no=@Case_no,Title=@Title,Case_type=@Case_type,Status=@Status,Filed_date=@Filed_date,Client_id=@Client_id,Judge_id=@Judge_id WHERE Case_id=@Case_id;
        ELSE PRINT 'Error: Not found.';
    END""",
    "CREATE OR ALTER PROCEDURE update_case_status @Case_id INT, @Status VARCHAR(50) AS BEGIN IF EXISTS (SELECT 1 FROM [Case] WHERE Case_id=@Case_id) UPDATE [Case] SET Status=@Status WHERE Case_id=@Case_id; ELSE PRINT 'Error: Not found.'; END",
    "CREATE OR ALTER PROCEDURE delete_case @Case_id INT AS BEGIN IF EXISTS (SELECT 1 FROM [Case] WHERE Case_id=@Case_id) DELETE FROM [Case] WHERE Case_id=@Case_id; ELSE PRINT 'Error: Not found.'; END",

    """CREATE OR ALTER PROCEDURE assign_lawyer_to_case
        @id INT, @Case_id INT, @Lawyer_id INT, @Assigned_date DATE, @Role VARCHAR(100)
    AS BEGIN
        IF EXISTS (SELECT 1 FROM Case_Lawyer WHERE id=@id)
            BEGIN PRINT 'Error: ID exists.'; RETURN; END
        INSERT INTO Case_Lawyer VALUES (@id,@Case_id,@Lawyer_id,@Assigned_date,@Role);
    END""",
    "CREATE OR ALTER PROCEDURE get_all_assignments AS BEGIN SELECT * FROM Case_Lawyer; END",
    "CREATE OR ALTER PROCEDURE get_assignment_by_id @id INT AS BEGIN SELECT * FROM Case_Lawyer WHERE id=@id; END",
    "CREATE OR ALTER PROCEDURE get_lawyers_for_case @Case_id INT AS BEGIN SELECT * FROM Case_Lawyer WHERE Case_id=@Case_id; END",
    "CREATE OR ALTER PROCEDURE get_cases_for_lawyer @Lawyer_id INT AS BEGIN SELECT * FROM Case_Lawyer WHERE Lawyer_id=@Lawyer_id; END",
    """CREATE OR ALTER PROCEDURE update_assignment
        @Old_Case_id INT, @Old_Lawyer_id INT, @New_Case_id INT, @New_Lawyer_id INT
    AS BEGIN
        UPDATE Case_Lawyer SET Case_id=@New_Case_id,Lawyer_id=@New_Lawyer_id
        WHERE Case_id=@Old_Case_id AND Lawyer_id=@Old_Lawyer_id;
    END""",
    "CREATE OR ALTER PROCEDURE delete_assignment @Case_id INT, @Lawyer_id INT AS BEGIN DELETE FROM Case_Lawyer WHERE Case_id=@Case_id AND Lawyer_id=@Lawyer_id; END",

    """CREATE OR ALTER PROCEDURE add_timeline_entry
        @Entry_id INT, @Case_id INT, @Hearing_date DATE, @Next_date DATE,
        @Proceeding_type VARCHAR(100), @Outcome VARCHAR(200), @Note VARCHAR(300)
    AS BEGIN
        IF EXISTS (SELECT 1 FROM Timeline WHERE Entry_id=@Entry_id)
            BEGIN PRINT 'Error: ID exists.'; RETURN; END
        INSERT INTO Timeline VALUES (@Entry_id,@Case_id,@Hearing_date,@Next_date,@Proceeding_type,@Outcome,@Note);
    END""",
    "CREATE OR ALTER PROCEDURE get_all_timeline_entries AS BEGIN SELECT * FROM Timeline; END",
    "CREATE OR ALTER PROCEDURE get_timeline_entry_by_id @Entry_id INT AS BEGIN SELECT * FROM Timeline WHERE Entry_id=@Entry_id; END",
    "CREATE OR ALTER PROCEDURE get_timeline_for_case @Case_id INT AS BEGIN SELECT * FROM Timeline WHERE Case_id=@Case_id; END",
    """CREATE OR ALTER PROCEDURE update_timeline_entry
        @Entry_id INT, @Case_id INT, @Hearing_date DATE, @Next_date DATE,
        @Proceeding_type VARCHAR(100), @Outcome VARCHAR(200), @Note VARCHAR(300)
    AS BEGIN
        IF EXISTS (SELECT 1 FROM Timeline WHERE Entry_id=@Entry_id)
            UPDATE Timeline SET Case_id=@Case_id,Hearing_date=@Hearing_date,Next_date=@Next_date,Proceeding_type=@Proceeding_type,Outcome=@Outcome,Note=@Note WHERE Entry_id=@Entry_id;
        ELSE PRINT 'Error: Not found.';
    END""",
    "CREATE OR ALTER PROCEDURE delete_timeline_entry @Entry_id INT AS BEGIN IF EXISTS (SELECT 1 FROM Timeline WHERE Entry_id=@Entry_id) DELETE FROM Timeline WHERE Entry_id=@Entry_id; ELSE PRINT 'Error: Not found.'; END",

    """CREATE OR ALTER PROCEDURE add_journal_entry
        @Journal_id INT, @Case_id INT, @Lawyer_id INT, @Entry_date DATE,
        @Entry_type VARCHAR(100), @Content VARCHAR(500)
    AS BEGIN
        IF EXISTS (SELECT 1 FROM Journal WHERE Journal_id=@Journal_id)
            BEGIN PRINT 'Error: ID exists.'; RETURN; END
        INSERT INTO Journal VALUES (@Journal_id,@Case_id,@Lawyer_id,@Entry_date,@Entry_type,@Content);
    END""",
    "CREATE OR ALTER PROCEDURE get_all_journals AS BEGIN SELECT * FROM Journal; END",
    "CREATE OR ALTER PROCEDURE get_journal_by_id @Journal_id INT AS BEGIN SELECT * FROM Journal WHERE Journal_id=@Journal_id; END",
    "CREATE OR ALTER PROCEDURE get_journal_for_case @Case_id INT AS BEGIN SELECT * FROM Journal WHERE Case_id=@Case_id; END",
    """CREATE OR ALTER PROCEDURE update_journal_entry
        @Journal_id INT, @Case_id INT, @Lawyer_id INT, @Entry_date DATE,
        @Entry_type VARCHAR(100), @Content VARCHAR(500)
    AS BEGIN
        IF EXISTS (SELECT 1 FROM Journal WHERE Journal_id=@Journal_id)
            UPDATE Journal SET Case_id=@Case_id,Lawyer_id=@Lawyer_id,Entry_date=@Entry_date,Entry_type=@Entry_type,Content=@Content WHERE Journal_id=@Journal_id;
        ELSE PRINT 'Error: Not found.';
    END""",
    "CREATE OR ALTER PROCEDURE delete_journal_entry @Journal_id INT AS BEGIN IF EXISTS (SELECT 1 FROM Journal WHERE Journal_id=@Journal_id) DELETE FROM Journal WHERE Journal_id=@Journal_id; ELSE PRINT 'Error: Not found.'; END",

    """CREATE OR ALTER PROCEDURE add_evidence
        @Evidence_id INT, @Case_id INT, @Title VARCHAR(150), @Evidence_type VARCHAR(100),
        @Description VARCHAR(300), @Submitted_date DATE, @File_path VARCHAR(300)
    AS BEGIN
        IF EXISTS (SELECT 1 FROM Evidence WHERE Evidence_id=@Evidence_id)
            BEGIN PRINT 'Error: ID exists.'; RETURN; END
        INSERT INTO Evidence VALUES (@Evidence_id,@Case_id,@Title,@Evidence_type,@Description,@Submitted_date,@File_path);
    END""",
    "CREATE OR ALTER PROCEDURE get_all_evidence AS BEGIN SELECT * FROM Evidence; END",
    "CREATE OR ALTER PROCEDURE get_evidence_by_id @Evidence_id INT AS BEGIN SELECT * FROM Evidence WHERE Evidence_id=@Evidence_id; END",
    "CREATE OR ALTER PROCEDURE get_evidence_for_case @Case_id INT AS BEGIN SELECT * FROM Evidence WHERE Case_id=@Case_id; END",
    "CREATE OR ALTER PROCEDURE get_evidence_by_title @Title VARCHAR(150) AS BEGIN SELECT * FROM Evidence WHERE Title=@Title; END",
    """CREATE OR ALTER PROCEDURE update_evidence
        @Evidence_id INT, @Case_id INT, @Title VARCHAR(150), @Evidence_type VARCHAR(100),
        @Description VARCHAR(300), @Submitted_date DATE, @File_path VARCHAR(300)
    AS BEGIN
        IF EXISTS (SELECT 1 FROM Evidence WHERE Evidence_id=@Evidence_id)
            UPDATE Evidence SET Case_id=@Case_id,Title=@Title,Evidence_type=@Evidence_type,Description=@Description,Submitted_date=@Submitted_date,File_path=@File_path WHERE Evidence_id=@Evidence_id;
        ELSE PRINT 'Error: Not found.';
    END""",
    "CREATE OR ALTER PROCEDURE delete_evidence @Evidence_id INT AS BEGIN IF EXISTS (SELECT 1 FROM Evidence WHERE Evidence_id=@Evidence_id) DELETE FROM Evidence WHERE Evidence_id=@Evidence_id; ELSE PRINT 'Error: Not found.'; END",

    """CREATE OR ALTER PROCEDURE add_payment
        @Payment_id INT, @Case_id INT, @Lawyer_id INT, @Client_id INT,
        @Amount DECIMAL(10,2), @Payment_date DATE, @Status VARCHAR(50), @Description VARCHAR(300)
    AS BEGIN
        IF EXISTS (SELECT 1 FROM Payment WHERE Payment_id=@Payment_id)
            BEGIN PRINT 'Error: ID exists.'; RETURN; END
        INSERT INTO Payment VALUES (@Payment_id,@Case_id,@Lawyer_id,@Client_id,@Amount,@Payment_date,@Status,@Description);
    END""",
    "CREATE OR ALTER PROCEDURE get_all_payments AS BEGIN SELECT * FROM Payment; END",
    "CREATE OR ALTER PROCEDURE get_payment_by_id @Payment_id INT AS BEGIN SELECT * FROM Payment WHERE Payment_id=@Payment_id; END",
    "CREATE OR ALTER PROCEDURE get_payments_for_case @Case_id INT AS BEGIN SELECT * FROM Payment WHERE Case_id=@Case_id; END",
    """CREATE OR ALTER PROCEDURE update_payment
        @Payment_id INT, @Case_id INT, @Lawyer_id INT, @Client_id INT,
        @Amount DECIMAL(10,2), @Payment_date DATE, @Status VARCHAR(50), @Description VARCHAR(300)
    AS BEGIN
        IF EXISTS (SELECT 1 FROM Payment WHERE Payment_id=@Payment_id)
            UPDATE Payment SET Case_id=@Case_id,Lawyer_id=@Lawyer_id,Client_id=@Client_id,Amount=@Amount,Payment_date=@Payment_date,Status=@Status,Description=@Description WHERE Payment_id=@Payment_id;
        ELSE PRINT 'Error: Not found.';
    END""",
    "CREATE OR ALTER PROCEDURE update_payment_status @Payment_id INT, @Status VARCHAR(50) AS BEGIN IF EXISTS (SELECT 1 FROM Payment WHERE Payment_id=@Payment_id) UPDATE Payment SET Status=@Status WHERE Payment_id=@Payment_id; ELSE PRINT 'Error: Not found.'; END",
    "CREATE OR ALTER PROCEDURE delete_payment @Payment_id INT AS BEGIN IF EXISTS (SELECT 1 FROM Payment WHERE Payment_id=@Payment_id) DELETE FROM Payment WHERE Payment_id=@Payment_id; ELSE PRINT 'Error: Not found.'; END",
    "CREATE OR ALTER PROCEDURE get_total_paid_amount @Case_id INT AS BEGIN SELECT ISNULL(SUM(Amount),0) AS Total_Paid FROM Payment WHERE Case_id=@Case_id AND Status='Paid'; END",
]

# DB Connection
@st.cache_resource
def setup_db():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=HadiaLaraib\\SQLEXPRESS;"
        "DATABASE=master;"
        "Trusted_Connection=yes;"
    )
    cur = conn.cursor()
    for proc in PROCEDURES:
        cur.execute(proc)
    conn.commit()
    return conn

conn = setup_db()

# Validation
def is_valid_name(v):
    return v.strip() != "" and all(c.isalpha() or c == " " for c in v)

def is_valid_email(v):
    return "@" in v and "." in v

def is_valid_phone(v):
    return v.isdigit() and 10 <= len(v) <= 15

def is_valid_cnic(v):
    p = v.split("-")
    return (len(p) == 3 and len(p[0]) == 5 and len(p[1]) == 7
            and len(p[2]) == 1 and all(x.isdigit() for x in p))

def is_valid_amount(v):
    return v > 0

# DB Helpers 
def read_proc(sql, params=()):
    cur = conn.cursor()
    cur.execute(sql, params)
    try:
        return cur.fetchall()
    except pyodbc.ProgrammingError:
        return []

def write_proc(sql, params=()):
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()

def rec_exists(proc, param, val):
    return len(read_proc(f"EXEC {proc} {param}=?", (val,))) > 0

def lawyer_in_case(case_id, lawyer_id):
    return len(read_proc(
        "SELECT 1 FROM Case_Lawyer WHERE Case_id=? AND Lawyer_id=?", (case_id, lawyer_id)
    )) > 0

def client_in_case(case_id, client_id):
    return len(read_proc(
        "SELECT 1 FROM [Case] WHERE Case_id=? AND Client_id=?", (case_id, client_id)
    )) > 0

def get_count(table):
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        return cur.fetchone()[0]
    except:
        return 0

def show_table(rows, entity):
    if rows:
        data = [dict(zip(COLS[entity], list(r))) for r in rows]
        st.dataframe(data, use_container_width=True)
    else:
        st.info("No records found in the database.")

# UI Helpers 
def page_header(icon, title, description):
    st.title(f"{icon} {title}")
    st.info(description)
    st.divider()

# Home / Dashboard 
def home_page():
    st.title("⚖️ Law Firm Management System")
    st.caption("Database Systems Lab Project | University of XYZ | 2026")
    st.divider()

    st.markdown("### 📊 Database Overview")
    st.markdown("Below is a live count of all records currently stored in the database.")
    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("⚖️  Judges",   get_count("Judge"))
    c2.metric("👤  Clients",  get_count("Client"))
    c3.metric("👨‍💼  Lawyers",  get_count("Lawyer"))
    c4.metric("📁  Cases",    get_count("[Case]"))

    c5, c6, c7, c8 = st.columns(4)
    c5.metric("🔗  Assignments", get_count("Case_Lawyer"))
    c6.metric("🕐  Timeline",    get_count("Timeline"))
    c7.metric("📓  Journal",     get_count("Journal"))
    c8.metric("💰  Payments",    get_count("Payment"))

    st.markdown("---")
    st.markdown("### 📖 How to Use This System")
    st.markdown("""
    1. **Select a module** from the left sidebar (e.g. Judge, Client, Case, etc.)
    2. Each module has **tabs** at the top for different actions:
       - **Add** → Fill the form to insert a new record
       - **View All** → Click the button to see all records in a table
       - **Search** → Enter an ID and click Search to find one record
       - **Update** → Enter the ID you want to change, then fill new values
       - **Delete** → Enter the ID you want to remove and confirm
    3. The system **validates your input** — if something is wrong, a red error message appears
    4. A **green success message** means the operation was completed successfully
    """)

    st.markdown("---")
    st.markdown("### 🗃️ System Modules")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**⚖️ Judge** — Manage court judges")
        st.markdown("**👤 Client** — Manage law firm clients")
        st.markdown("**👨‍💼 Lawyer** — Manage lawyers and their details")
    with col2:
        st.markdown("**📁 Case** — Manage legal cases")
        st.markdown("**🔗 Case-Lawyer** — Assign lawyers to cases")
        st.markdown("**🕐 Timeline** — Track case hearing dates")
    with col3:
        st.markdown("**📓 Journal** — Lawyer notes per case")
        st.markdown("**🔍 Evidence** — Manage case evidence")
        st.markdown("**💰 Payment** — Track client payments")


# Judge Page 
def judge_page():
    page_header("⚖️", "Judge Management",
                "Use this section to Add, View, Search, Update, or Delete judge records.")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["➕ Add Judge", "📋 View All", "🔍 Search by ID", "✏️ Update", "🗑️ Delete"]
    )

    with tab1:
        st.markdown("#### Add a New Judge")
        with st.form("judge_add"):
            c1, c2 = st.columns(2)
            judge_id    = c1.number_input("Judge ID", min_value=1, step=1, help="Unique number, e.g. 1")
            name        = c2.text_input("Full Name", placeholder="e.g. Justice Ahmad", help="Letters only")
            c3, c4 = st.columns(2)
            court_name     = c3.text_input("Court Name", placeholder="e.g. Lahore High Court")
            specialization = c4.text_input("Specialization", placeholder="e.g. Criminal")
            contact_info   = st.text_input("Email Address", placeholder="e.g. judge@court.com")

            if st.form_submit_button("✅ Add Judge", use_container_width=True):
                jid = int(judge_id)
                if rec_exists("get_judge_by_id", "@Judge_id", jid):
                    st.error("❌ Judge ID already exists. Choose a different ID.")
                elif not is_valid_name(name):
                    st.error("❌ Name must contain only letters and spaces.")
                elif rec_exists("get_judge_by_name", "@Name", name):
                    st.error("❌ A judge with this name already exists.")
                elif not is_valid_name(court_name):
                    st.error("❌ Court Name must contain only letters and spaces.")
                elif not is_valid_name(specialization):
                    st.error("❌ Specialization must contain only letters and spaces.")
                elif not is_valid_email(contact_info):
                    st.error("❌ Email must contain '@' and '.' — e.g. judge@court.com")
                else:
                    write_proc("EXEC add_judge @Judge_id=?,@Name=?,@Court_name=?,@Specialization=?,@Contact_info=?",
                               (jid, name, court_name, specialization, contact_info))
                    st.success("✅ Judge added successfully!")

    with tab2:
        st.markdown("#### All Judges in Database")
        if st.button("📋 Load All Judges", use_container_width=True):
            show_table(read_proc("EXEC get_all_judges"), "Judge")

    with tab3:
        st.markdown("#### Search Judge by ID")
        jid = int(st.number_input("Enter Judge ID to search", min_value=1, step=1, key="judge_s"))
        if st.button("🔍 Search", use_container_width=True, key="judge_sb"):
            show_table(read_proc("EXEC get_judge_by_id @Judge_id=?", (jid,)), "Judge")

    with tab4:
        st.markdown("#### Update an Existing Judge")
        st.caption("Enter the Judge ID you want to update, then provide the new values below.")
        with st.form("judge_upd"):
            judge_id = st.number_input("Judge ID to Update", min_value=1, step=1)
            c1, c2 = st.columns(2)
            name        = c1.text_input("New Full Name")
            court_name  = c2.text_input("New Court Name")
            c3, c4 = st.columns(2)
            specialization = c3.text_input("New Specialization")
            contact_info   = c4.text_input("New Email Address")

            if st.form_submit_button("✏️ Update Judge", use_container_width=True):
                jid = int(judge_id)
                if not rec_exists("get_judge_by_id", "@Judge_id", jid):
                    st.error("❌ No judge found with this ID.")
                elif not is_valid_name(name):
                    st.error("❌ Name must contain only letters and spaces.")
                elif not is_valid_name(court_name):
                    st.error("❌ Court Name must contain only letters and spaces.")
                elif not is_valid_name(specialization):
                    st.error("❌ Specialization must contain only letters and spaces.")
                elif not is_valid_email(contact_info):
                    st.error("❌ Email must contain '@' and '.'")
                else:
                    write_proc("EXEC update_judge @Judge_id=?,@Name=?,@Court_name=?,@Specialization=?,@Contact_info=?",
                               (jid, name, court_name, specialization, contact_info))
                    st.success("✅ Judge updated successfully!")

    with tab5:
        st.markdown("#### Delete a Judge")
        st.warning("⚠️ This action is permanent and cannot be undone.")
        with st.form("judge_del"):
            judge_id = st.number_input("Judge ID to Delete", min_value=1, step=1)
            if st.form_submit_button("🗑️ Delete Judge", use_container_width=True, type="primary"):
                jid = int(judge_id)
                if not rec_exists("get_judge_by_id", "@Judge_id", jid):
                    st.error("❌ No judge found with this ID.")
                else:
                    write_proc("EXEC delete_judge @Judge_id=?", (jid,))
                    st.success("✅ Judge deleted successfully!")


#  Client Page 
def client_page():
    page_header("👤", "Client Management",
                "Manage all clients of the law firm — add new clients, search, update, or remove records.")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["➕ Add Client", "📋 View All", "🔍 Search by ID", "✏️ Update", "🗑️ Delete"]
    )

    with tab1:
        st.markdown("#### Add a New Client")
        with st.form("client_add"):
            c1, c2 = st.columns(2)
            client_id = c1.number_input("Client ID", min_value=1, step=1)
            name      = c2.text_input("Full Name", placeholder="e.g. Hamza Ali")
            c3, c4 = st.columns(2)
            cnic     = c3.text_input("CNIC", placeholder="XXXXX-XXXXXXX-X")
            phone_no = c4.text_input("Phone Number", placeholder="03001234567")
            c5, c6 = st.columns(2)
            email  = c5.text_input("Email", placeholder="client@gmail.com")
            street = c6.text_input("Street", placeholder="Street 1, Block A")
            city   = st.text_input("City", placeholder="e.g. Lahore")

            if st.form_submit_button("✅ Add Client", use_container_width=True):
                cid = int(client_id)
                if rec_exists("get_client_by_id", "@Client_id", cid):
                    st.error("❌ Client ID already exists.")
                elif not is_valid_name(name):
                    st.error("❌ Name must contain only letters and spaces.")
                elif rec_exists("get_client_by_name", "@Name", name):
                    st.error("❌ A client with this name already exists.")
                elif not is_valid_cnic(cnic):
                    st.error("❌ CNIC format must be XXXXX-XXXXXXX-X (with dashes).")
                elif not is_valid_phone(phone_no):
                    st.error("❌ Phone must be digits only, 10 to 15 digits long.")
                elif not is_valid_email(email):
                    st.error("❌ Email must contain '@' and '.'")
                elif street.strip() == "":
                    st.error("❌ Street cannot be empty.")
                elif not is_valid_name(city):
                    st.error("❌ City must contain only letters and spaces.")
                else:
                    write_proc("EXEC add_client @Client_id=?,@Name=?,@CNIC=?,@Phone_no=?,@Email=?,@Street=?,@City=?",
                               (cid, name, cnic, phone_no, email, street, city))
                    st.success("✅ Client added successfully!")

    with tab2:
        st.markdown("#### All Clients in Database")
        if st.button("📋 Load All Clients", use_container_width=True):
            show_table(read_proc("EXEC get_all_clients"), "Client")

    with tab3:
        st.markdown("#### Search Client by ID")
        cid = int(st.number_input("Enter Client ID", min_value=1, step=1, key="client_s"))
        if st.button("🔍 Search", use_container_width=True, key="client_sb"):
            show_table(read_proc("EXEC get_client_by_id @Client_id=?", (cid,)), "Client")

    with tab4:
        st.markdown("#### Update an Existing Client")
        with st.form("client_upd"):
            client_id = st.number_input("Client ID to Update", min_value=1, step=1)
            c1, c2 = st.columns(2)
            name     = c1.text_input("New Name")
            cnic     = c2.text_input("New CNIC", placeholder="XXXXX-XXXXXXX-X")
            c3, c4 = st.columns(2)
            phone_no = c3.text_input("New Phone Number")
            email    = c4.text_input("New Email")
            c5, c6 = st.columns(2)
            street   = c5.text_input("New Street")
            city     = c6.text_input("New City")

            if st.form_submit_button("✏️ Update Client", use_container_width=True):
                cid = int(client_id)
                if not rec_exists("get_client_by_id", "@Client_id", cid):
                    st.error("❌ No client found with this ID.")
                elif not is_valid_name(name):
                    st.error("❌ Name must contain only letters and spaces.")
                elif not is_valid_cnic(cnic):
                    st.error("❌ CNIC format must be XXXXX-XXXXXXX-X.")
                elif not is_valid_phone(phone_no):
                    st.error("❌ Phone must be digits only, 10-15 digits.")
                elif not is_valid_email(email):
                    st.error("❌ Email must contain '@' and '.'")
                elif street.strip() == "":
                    st.error("❌ Street cannot be empty.")
                elif not is_valid_name(city):
                    st.error("❌ City must contain only letters and spaces.")
                else:
                    write_proc("EXEC update_client @Client_id=?,@Name=?,@CNIC=?,@Phone_no=?,@Email=?,@Street=?,@City=?",
                               (cid, name, cnic, phone_no, email, street, city))
                    st.success("✅ Client updated successfully!")

    with tab5:
        st.markdown("#### Delete a Client")
        st.warning("⚠️ This action is permanent and cannot be undone.")
        with st.form("client_del"):
            client_id = st.number_input("Client ID to Delete", min_value=1, step=1)
            if st.form_submit_button("🗑️ Delete Client", use_container_width=True, type="primary"):
                cid = int(client_id)
                if not rec_exists("get_client_by_id", "@Client_id", cid):
                    st.error("❌ No client found with this ID.")
                else:
                    write_proc("EXEC delete_client @Client_id=?", (cid,))
                    st.success("✅ Client deleted successfully!")


#  Lawyer Page 
def lawyer_page():
    page_header("👨‍💼", "Lawyer Management",
                "Add, view, search, update, or delete lawyer records from the law firm database.")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["➕ Add Lawyer", "📋 View All", "🔍 Search by ID", "✏️ Update", "🗑️ Delete"]
    )

    with tab1:
        st.markdown("#### Add a New Lawyer")
        with st.form("lawyer_add"):
            c1, c2 = st.columns(2)
            lawyer_id      = c1.number_input("Lawyer ID", min_value=1, step=1)
            name           = c2.text_input("Full Name", placeholder="e.g. Ali Raza")
            c3, c4 = st.columns(2)
            specialization = c3.text_input("Specialization", placeholder="e.g. Criminal Law")
            bar_number     = c4.text_input("Bar Number", placeholder="e.g. BAR101")
            c5, c6 = st.columns(2)
            phone_no       = c5.text_input("Phone Number", placeholder="03001234567")
            email          = c6.text_input("Email", placeholder="lawyer@firm.com")
            hourly_rate    = st.number_input("Hourly Rate (PKR)", min_value=0.01, step=100.0, format="%.2f")

            if st.form_submit_button("✅ Add Lawyer", use_container_width=True):
                lid = int(lawyer_id)
                if rec_exists("get_lawyer_by_id", "@Lawyer_id", lid):
                    st.error("❌ Lawyer ID already exists.")
                elif not is_valid_name(name):
                    st.error("❌ Name must contain only letters and spaces.")
                elif rec_exists("get_lawyer_by_name", "@Name", name):
                    st.error("❌ A lawyer with this name already exists.")
                elif not is_valid_name(specialization):
                    st.error("❌ Specialization must contain only letters and spaces.")
                elif bar_number.strip() == "":
                    st.error("❌ Bar Number cannot be empty.")
                elif not is_valid_phone(phone_no):
                    st.error("❌ Phone must be digits only, 10-15 digits.")
                elif not is_valid_email(email):
                    st.error("❌ Email must contain '@' and '.'")
                elif not is_valid_amount(hourly_rate):
                    st.error("❌ Hourly Rate must be greater than 0.")
                else:
                    write_proc("EXEC add_lawyer @Lawyer_id=?,@Name=?,@Email=?,@Bar_number=?,@Specialization=?,@Phone_no=?,@Hourly_rate=?",
                               (lid, name, email, bar_number, specialization, phone_no, hourly_rate))
                    st.success("✅ Lawyer added successfully!")

    with tab2:
        st.markdown("#### All Lawyers in Database")
        if st.button("📋 Load All Lawyers", use_container_width=True):
            show_table(read_proc("EXEC get_all_lawyers"), "Lawyer")

    with tab3:
        st.markdown("#### Search Lawyer by ID")
        lid = int(st.number_input("Enter Lawyer ID", min_value=1, step=1, key="lawyer_s"))
        if st.button("🔍 Search", use_container_width=True, key="lawyer_sb"):
            show_table(read_proc("EXEC get_lawyer_by_id @Lawyer_id=?", (lid,)), "Lawyer")

    with tab4:
        st.markdown("#### Update an Existing Lawyer")
        with st.form("lawyer_upd"):
            lawyer_id = st.number_input("Lawyer ID to Update", min_value=1, step=1)
            c1, c2 = st.columns(2)
            name           = c1.text_input("New Name")
            specialization = c2.text_input("New Specialization")
            c3, c4 = st.columns(2)
            phone_no    = c3.text_input("New Phone Number")
            email       = c4.text_input("New Email")
            c5, c6 = st.columns(2)
            bar_number  = c5.text_input("New Bar Number")
            hourly_rate = c6.number_input("New Hourly Rate (PKR)", min_value=0.01, step=100.0, format="%.2f")

            if st.form_submit_button("✏️ Update Lawyer", use_container_width=True):
                lid = int(lawyer_id)
                if not rec_exists("get_lawyer_by_id", "@Lawyer_id", lid):
                    st.error("❌ No lawyer found with this ID.")
                elif not is_valid_name(name):
                    st.error("❌ Name must contain only letters and spaces.")
                elif not is_valid_name(specialization):
                    st.error("❌ Specialization must contain only letters and spaces.")
                elif not is_valid_phone(phone_no):
                    st.error("❌ Phone must be digits only, 10-15 digits.")
                elif not is_valid_email(email):
                    st.error("❌ Email must contain '@' and '.'")
                elif bar_number.strip() == "":
                    st.error("❌ Bar Number cannot be empty.")
                elif not is_valid_amount(hourly_rate):
                    st.error("❌ Hourly Rate must be greater than 0.")
                else:
                    write_proc("EXEC update_lawyer @Lawyer_id=?,@Name=?,@Email=?,@Bar_number=?,@Specialization=?,@Phone_no=?,@Hourly_rate=?",
                               (lid, name, email, bar_number, specialization, phone_no, hourly_rate))
                    st.success("✅ Lawyer updated successfully!")

    with tab5:
        st.markdown("#### Delete a Lawyer")
        st.warning("⚠️ This action is permanent and cannot be undone.")
        with st.form("lawyer_del"):
            lawyer_id = st.number_input("Lawyer ID to Delete", min_value=1, step=1)
            if st.form_submit_button("🗑️ Delete Lawyer", use_container_width=True, type="primary"):
                lid = int(lawyer_id)
                if not rec_exists("get_lawyer_by_id", "@Lawyer_id", lid):
                    st.error("❌ No lawyer found with this ID.")
                else:
                    write_proc("EXEC delete_lawyer @Lawyer_id=?", (lid,))
                    st.success("✅ Lawyer deleted successfully!")


# Case Page
def case_page():
    page_header("📁", "Case Management",
                "Manage all legal cases. A case must have a valid Client ID and Judge ID already in the system.")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "➕ Add", "📋 View All", "🔍 By ID", "👤 By Client",
        "📊 By Status", "✏️ Update", "🔄 Update Status", "🗑️ Delete"
    ])

    with tab1:
        st.markdown("#### Add a New Case")
        with st.form("case_add"):
            c1, c2, c3 = st.columns(3)
            case_id   = c1.number_input("Case ID", min_value=1, step=1)
            client_id = c2.number_input("Client ID", min_value=1, step=1, help="Must already exist")
            judge_id  = c3.number_input("Judge ID", min_value=1, step=1, help="Must already exist")
            c4, c5 = st.columns(2)
            case_no   = c4.text_input("Case No", placeholder="e.g. 101 (digits only)")
            title     = c5.text_input("Case Name/Title", placeholder="e.g. Property Dispute")
            c6, c7, c8 = st.columns(3)
            case_type  = c6.text_input("Case Type", placeholder="e.g. Civil")
            status     = c7.selectbox("Status", ["Open", "Pending", "Closed"])
            filed_date = c8.date_input("Filed Date")

            if st.form_submit_button("✅ Add Case", use_container_width=True):
                cid, clid, jid = int(case_id), int(client_id), int(judge_id)
                if rec_exists("get_case_by_id", "@Case_id", cid):
                    st.error("❌ Case ID already exists.")
                elif not rec_exists("get_client_by_id", "@Client_id", clid):
                    st.error("❌ Client ID does not exist. Add the client first.")
                elif not rec_exists("get_judge_by_id", "@Judge_id", jid):
                    st.error("❌ Judge ID does not exist. Add the judge first.")
                elif not case_no.isdigit():
                    st.error("❌ Case No must be digits only (e.g. 101).")
                elif title.strip() == "":
                    st.error("❌ Case Name cannot be empty.")
                elif rec_exists("get_case_by_title", "@Title", title):
                    st.error("❌ A case with this name already exists.")
                elif not is_valid_name(case_type):
                    st.error("❌ Case Type must contain only letters and spaces.")
                else:
                    write_proc("EXEC add_case @Case_id=?,@Case_no=?,@Client_id=?,@Judge_id=?,@Title=?,@Case_type=?,@Status=?,@Filed_date=?",
                               (cid, case_no, clid, jid, title, case_type, status, filed_date.isoformat()))
                    st.success("✅ Case added successfully!")

    with tab2:
        st.markdown("#### All Cases in Database")
        if st.button("📋 Load All Cases", use_container_width=True):
            show_table(read_proc("EXEC get_all_cases"), "Case")

    with tab3:
        st.markdown("#### Search Case by ID")
        cid = int(st.number_input("Case ID", min_value=1, step=1, key="case_s"))
        if st.button("🔍 Search", use_container_width=True, key="case_sb"):
            show_table(read_proc("EXEC get_case_by_id @Case_id=?", (cid,)), "Case")

    with tab4:
        st.markdown("#### Search Cases by Client ID")
        clid = int(st.number_input("Client ID", min_value=1, step=1, key="case_cl"))
        if st.button("🔍 Search by Client", use_container_width=True):
            if not rec_exists("get_client_by_id", "@Client_id", clid):
                st.error("❌ Client ID does not exist.")
            else:
                show_table(read_proc("EXEC get_cases_by_client @Client_id=?", (clid,)), "Case")

    with tab5:
        st.markdown("#### Search Cases by Status")
        status_s = st.selectbox("Select Status", ["Open", "Pending", "Closed"], key="case_st")
        if st.button("🔍 Search by Status", use_container_width=True):
            show_table(read_proc("EXEC get_cases_by_status @Status=?", (status_s,)), "Case")

    with tab6:
        st.markdown("#### Update an Existing Case")
        with st.form("case_upd"):
            c1, c2, c3 = st.columns(3)
            case_id   = c1.number_input("Case ID to Update", min_value=1, step=1)
            client_id = c2.number_input("New Client ID", min_value=1, step=1)
            judge_id  = c3.number_input("New Judge ID", min_value=1, step=1)
            c4, c5 = st.columns(2)
            case_no   = c4.text_input("New Case No (digits only)")
            title     = c5.text_input("New Case Name")
            c6, c7, c8 = st.columns(3)
            case_type  = c6.text_input("New Case Type")
            status     = c7.selectbox("New Status", ["Open", "Pending", "Closed"])
            filed_date = c8.date_input("New Filed Date")

            if st.form_submit_button("✏️ Update Case", use_container_width=True):
                cid, clid, jid = int(case_id), int(client_id), int(judge_id)
                if not rec_exists("get_case_by_id", "@Case_id", cid):
                    st.error("❌ No case found with this ID.")
                elif not rec_exists("get_client_by_id", "@Client_id", clid):
                    st.error("❌ Client ID does not exist.")
                elif not rec_exists("get_judge_by_id", "@Judge_id", jid):
                    st.error("❌ Judge ID does not exist.")
                elif not case_no.isdigit():
                    st.error("❌ Case No must be digits only.")
                elif title.strip() == "":
                    st.error("❌ Case Name cannot be empty.")
                elif not is_valid_name(case_type):
                    st.error("❌ Case Type must contain only letters and spaces.")
                else:
                    write_proc("EXEC update_case @Case_id=?,@Case_no=?,@Client_id=?,@Judge_id=?,@Title=?,@Case_type=?,@Status=?,@Filed_date=?",
                               (cid, case_no, clid, jid, title, case_type, status, filed_date.isoformat()))
                    st.success("✅ Case updated successfully!")

    with tab7:
        st.markdown("#### Update Case Status Only")
        st.caption("Use this to quickly change the status of a case without editing everything else.")
        with st.form("case_status_upd"):
            c1, c2 = st.columns(2)
            case_id    = c1.number_input("Case ID", min_value=1, step=1)
            new_status = c2.selectbox("New Status", ["Open", "Pending", "Closed"])
            if st.form_submit_button("🔄 Update Status", use_container_width=True):
                cid = int(case_id)
                if not rec_exists("get_case_by_id", "@Case_id", cid):
                    st.error("❌ No case found with this ID.")
                else:
                    write_proc("EXEC update_case_status @Case_id=?,@Status=?", (cid, new_status))
                    st.success("✅ Case status updated successfully!")

    with tab8:
        st.markdown("#### Delete a Case")
        st.warning("⚠️ This action is permanent and cannot be undone.")
        with st.form("case_del"):
            case_id = st.number_input("Case ID to Delete", min_value=1, step=1)
            if st.form_submit_button("🗑️ Delete Case", use_container_width=True, type="primary"):
                cid = int(case_id)
                if not rec_exists("get_case_by_id", "@Case_id", cid):
                    st.error("❌ No case found with this ID.")
                else:
                    write_proc("EXEC delete_case @Case_id=?", (cid,))
                    st.success("✅ Case deleted successfully!")


# Case-Lawyer Page 
def case_lawyer_page():
    page_header("🔗", "Case-Lawyer Assignment",
                "Assign lawyers to cases. A lawyer must exist in the system before being assigned.")

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "➕ Assign", "📋 View All", "👨‍⚖️ Lawyers for Case",
        "📁 Cases for Lawyer", "✏️ Update", "🗑️ Delete"
    ])

    with tab1:
        st.markdown("#### Assign a Lawyer to a Case")
        with st.form("cl_assign"):
            c1, c2, c3 = st.columns(3)
            assign_id = c1.number_input("Assignment ID", min_value=1, step=1)
            case_id   = c2.number_input("Case ID", min_value=1, step=1)
            lawyer_id = c3.number_input("Lawyer ID", min_value=1, step=1)
            c4, c5 = st.columns(2)
            assigned_date = c4.date_input("Assigned Date")
            role          = c5.text_input("Role", placeholder="e.g. Lead Lawyer")

            if st.form_submit_button("✅ Assign Lawyer", use_container_width=True):
                aid, cid, lid = int(assign_id), int(case_id), int(lawyer_id)
                if rec_exists("get_assignment_by_id", "@id", aid):
                    st.error("❌ Assignment ID already exists.")
                elif not rec_exists("get_case_by_id", "@Case_id", cid):
                    st.error("❌ Case ID does not exist.")
                elif not rec_exists("get_lawyer_by_id", "@Lawyer_id", lid):
                    st.error("❌ Lawyer ID does not exist.")
                elif not is_valid_name(role):
                    st.error("❌ Role must contain only letters and spaces.")
                else:
                    write_proc("EXEC assign_lawyer_to_case @id=?,@Case_id=?,@Lawyer_id=?,@Assigned_date=?,@Role=?",
                               (aid, cid, lid, assigned_date.isoformat(), role))
                    st.success("✅ Lawyer assigned to case successfully!")

    with tab2:
        st.markdown("#### All Assignments")
        if st.button("📋 Load All Assignments", use_container_width=True):
            show_table(read_proc("EXEC get_all_assignments"), "CaseLawyer")

    with tab3:
        st.markdown("#### Which Lawyers are Assigned to a Case?")
        cid = int(st.number_input("Case ID", min_value=1, step=1, key="cl_case"))
        if st.button("🔍 Get Lawyers", use_container_width=True):
            if not rec_exists("get_case_by_id", "@Case_id", cid):
                st.error("❌ Case ID does not exist.")
            else:
                show_table(read_proc("EXEC get_lawyers_for_case @Case_id=?", (cid,)), "CaseLawyer")

    with tab4:
        st.markdown("#### Which Cases is a Lawyer Assigned to?")
        lid = int(st.number_input("Lawyer ID", min_value=1, step=1, key="cl_lawyer"))
        if st.button("🔍 Get Cases", use_container_width=True):
            if not rec_exists("get_lawyer_by_id", "@Lawyer_id", lid):
                st.error("❌ Lawyer ID does not exist.")
            else:
                show_table(read_proc("EXEC get_cases_for_lawyer @Lawyer_id=?", (lid,)), "CaseLawyer")

    with tab5:
        st.markdown("#### Update an Assignment")
        with st.form("cl_upd"):
            c1, c2 = st.columns(2)
            old_case_id   = c1.number_input("Current Case ID", min_value=1, step=1)
            old_lawyer_id = c2.number_input("Current Lawyer ID", min_value=1, step=1)
            c3, c4 = st.columns(2)
            new_case_id   = c3.number_input("New Case ID", min_value=1, step=1)
            new_lawyer_id = c4.number_input("New Lawyer ID", min_value=1, step=1)
            if st.form_submit_button("✏️ Update Assignment", use_container_width=True):
                ocid, olid = int(old_case_id), int(old_lawyer_id)
                ncid, nlid = int(new_case_id), int(new_lawyer_id)
                if not rec_exists("get_case_by_id", "@Case_id", ocid):
                    st.error("❌ Current Case ID does not exist.")
                elif not rec_exists("get_lawyer_by_id", "@Lawyer_id", olid):
                    st.error("❌ Current Lawyer ID does not exist.")
                elif not rec_exists("get_case_by_id", "@Case_id", ncid):
                    st.error("❌ New Case ID does not exist.")
                elif not rec_exists("get_lawyer_by_id", "@Lawyer_id", nlid):
                    st.error("❌ New Lawyer ID does not exist.")
                else:
                    write_proc("EXEC update_assignment @Old_Case_id=?,@Old_Lawyer_id=?,@New_Case_id=?,@New_Lawyer_id=?",
                               (ocid, olid, ncid, nlid))
                    st.success("✅ Assignment updated successfully!")

    with tab6:
        st.markdown("#### Remove an Assignment")
        st.warning("⚠️ This action is permanent.")
        with st.form("cl_del"):
            c1, c2 = st.columns(2)
            case_id   = c1.number_input("Case ID", min_value=1, step=1)
            lawyer_id = c2.number_input("Lawyer ID", min_value=1, step=1)
            if st.form_submit_button("🗑️ Delete Assignment", use_container_width=True, type="primary"):
                cid, lid = int(case_id), int(lawyer_id)
                if not rec_exists("get_case_by_id", "@Case_id", cid):
                    st.error("❌ Case ID does not exist.")
                elif not rec_exists("get_lawyer_by_id", "@Lawyer_id", lid):
                    st.error("❌ Lawyer ID does not exist.")
                else:
                    write_proc("EXEC delete_assignment @Case_id=?,@Lawyer_id=?", (cid, lid))
                    st.success("✅ Assignment deleted successfully!")


# Timeline Page
def timeline_page():
    page_header("🕐", "Case Timeline",
                "Record hearing dates and proceedings for each case. Each entry tracks what happened and what is next.")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["➕ Add Entry", "📋 View All", "🔍 For Case", "✏️ Update", "🗑️ Delete"]
    )

    with tab1:
        st.markdown("#### Add a New Timeline Entry")
        with st.form("tl_add"):
            c1, c2 = st.columns(2)
            entry_id = c1.number_input("Entry ID", min_value=1, step=1)
            case_id  = c2.number_input("Case ID", min_value=1, step=1)
            c3, c4 = st.columns(2)
            hearing_date = c3.date_input("Hearing Date")
            next_date    = c4.date_input("Next Hearing Date")
            c5, c6 = st.columns(2)
            proc_type = c5.text_input("Proceeding Type", placeholder="e.g. Hearing")
            outcome   = c6.text_input("Outcome", placeholder="e.g. Pending")
            note = st.text_area("Note / Remarks", placeholder="e.g. First hearing conducted")

            if st.form_submit_button("✅ Add Entry", use_container_width=True):
                eid, cid = int(entry_id), int(case_id)
                if rec_exists("get_timeline_entry_by_id", "@Entry_id", eid):
                    st.error("❌ Entry ID already exists.")
                elif not rec_exists("get_case_by_id", "@Case_id", cid):
                    st.error("❌ Case ID does not exist.")
                elif not is_valid_name(proc_type):
                    st.error("❌ Proceeding Type must contain only letters and spaces.")
                elif not is_valid_name(outcome):
                    st.error("❌ Outcome must contain only letters and spaces.")
                else:
                    write_proc("EXEC add_timeline_entry @Entry_id=?,@Case_id=?,@Hearing_date=?,@Next_date=?,@Proceeding_type=?,@Outcome=?,@Note=?",
                               (eid, cid, hearing_date.isoformat(), next_date.isoformat(), proc_type, outcome, note))
                    st.success("✅ Timeline entry added successfully!")

    with tab2:
        st.markdown("#### All Timeline Entries")
        if st.button("📋 Load All Entries", use_container_width=True):
            show_table(read_proc("EXEC get_all_timeline_entries"), "Timeline")

    with tab3:
        st.markdown("#### Timeline for a Specific Case")
        cid = int(st.number_input("Case ID", min_value=1, step=1, key="tl_case"))
        if st.button("🔍 Get Timeline", use_container_width=True):
            if not rec_exists("get_case_by_id", "@Case_id", cid):
                st.error("❌ Case ID does not exist.")
            else:
                show_table(read_proc("EXEC get_timeline_for_case @Case_id=?", (cid,)), "Timeline")

    with tab4:
        st.markdown("#### Update a Timeline Entry")
        with st.form("tl_upd"):
            c1, c2 = st.columns(2)
            entry_id = c1.number_input("Entry ID to Update", min_value=1, step=1)
            case_id  = c2.number_input("New Case ID", min_value=1, step=1)
            c3, c4 = st.columns(2)
            hearing_date = c3.date_input("New Hearing Date")
            next_date    = c4.date_input("New Next Date")
            c5, c6 = st.columns(2)
            proc_type = c5.text_input("New Proceeding Type")
            outcome   = c6.text_input("New Outcome")
            note = st.text_area("New Note")

            if st.form_submit_button("✏️ Update Entry", use_container_width=True):
                eid, cid = int(entry_id), int(case_id)
                if not rec_exists("get_timeline_entry_by_id", "@Entry_id", eid):
                    st.error("❌ Entry ID does not exist.")
                elif not rec_exists("get_case_by_id", "@Case_id", cid):
                    st.error("❌ Case ID does not exist.")
                elif not is_valid_name(proc_type):
                    st.error("❌ Proceeding Type must contain only letters and spaces.")
                elif not is_valid_name(outcome):
                    st.error("❌ Outcome must contain only letters and spaces.")
                else:
                    write_proc("EXEC update_timeline_entry @Entry_id=?,@Case_id=?,@Hearing_date=?,@Next_date=?,@Proceeding_type=?,@Outcome=?,@Note=?",
                               (eid, cid, hearing_date.isoformat(), next_date.isoformat(), proc_type, outcome, note))
                    st.success("✅ Timeline entry updated successfully!")

    with tab5:
        st.markdown("#### Delete a Timeline Entry")
        st.warning("⚠️ This action is permanent.")
        with st.form("tl_del"):
            entry_id = st.number_input("Entry ID to Delete", min_value=1, step=1)
            if st.form_submit_button("🗑️ Delete Entry", use_container_width=True, type="primary"):
                eid = int(entry_id)
                if not rec_exists("get_timeline_entry_by_id", "@Entry_id", eid):
                    st.error("❌ Entry ID does not exist.")
                else:
                    write_proc("EXEC delete_timeline_entry @Entry_id=?", (eid,))
                    st.success("✅ Timeline entry deleted successfully!")


#  Journal Page 
def journal_page():
    page_header("📓", "Case Journal",
                "Lawyers record case notes here. The lawyer must be assigned to the case before adding an entry.")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["➕ Add Entry", "📋 View All", "🔍 For Case", "✏️ Update", "🗑️ Delete"]
    )

    with tab1:
        st.markdown("#### Add a New Journal Entry")
        with st.form("jn_add"):
            c1, c2, c3 = st.columns(3)
            journal_id = c1.number_input("Journal ID", min_value=1, step=1)
            case_id    = c2.number_input("Case ID", min_value=1, step=1)
            lawyer_id  = c3.number_input("Lawyer ID", min_value=1, step=1, help="Must be assigned to this case")
            c4, c5 = st.columns(2)
            entry_date = c4.date_input("Entry Date")
            entry_type = c5.text_input("Entry Type", placeholder="e.g. Case Note")
            content    = st.text_area("Content / Notes", placeholder="Describe what happened...")

            if st.form_submit_button("✅ Add Journal Entry", use_container_width=True):
                jid, cid, lid = int(journal_id), int(case_id), int(lawyer_id)
                if rec_exists("get_journal_by_id", "@Journal_id", jid):
                    st.error("❌ Journal ID already exists.")
                elif not rec_exists("get_case_by_id", "@Case_id", cid):
                    st.error("❌ Case ID does not exist.")
                elif not rec_exists("get_lawyer_by_id", "@Lawyer_id", lid):
                    st.error("❌ Lawyer ID does not exist.")
                elif not lawyer_in_case(cid, lid):
                    st.error("❌ This lawyer is not assigned to this case. Go to Case-Lawyer to assign first.")
                elif not is_valid_name(entry_type):
                    st.error("❌ Entry Type must contain only letters and spaces.")
                elif content.strip() == "":
                    st.error("❌ Content cannot be empty.")
                else:
                    write_proc("EXEC add_journal_entry @Journal_id=?,@Case_id=?,@Lawyer_id=?,@Entry_date=?,@Entry_type=?,@Content=?",
                               (jid, cid, lid, entry_date.isoformat(), entry_type, content))
                    st.success("✅ Journal entry added successfully!")

    with tab2:
        st.markdown("#### All Journal Entries")
        if st.button("📋 Load All Entries", use_container_width=True):
            show_table(read_proc("EXEC get_all_journals"), "Journal")

    with tab3:
        st.markdown("#### Journal Entries for a Specific Case")
        cid = int(st.number_input("Case ID", min_value=1, step=1, key="jn_case"))
        if st.button("🔍 Get Journal", use_container_width=True):
            if not rec_exists("get_case_by_id", "@Case_id", cid):
                st.error("❌ Case ID does not exist.")
            else:
                show_table(read_proc("EXEC get_journal_for_case @Case_id=?", (cid,)), "Journal")

    with tab4:
        st.markdown("#### Update a Journal Entry")
        with st.form("jn_upd"):
            c1, c2, c3 = st.columns(3)
            journal_id = c1.number_input("Journal ID to Update", min_value=1, step=1)
            case_id    = c2.number_input("New Case ID", min_value=1, step=1)
            lawyer_id  = c3.number_input("New Lawyer ID", min_value=1, step=1)
            c4, c5 = st.columns(2)
            entry_date = c4.date_input("New Entry Date")
            entry_type = c5.text_input("New Entry Type")
            content    = st.text_area("New Content")

            if st.form_submit_button("✏️ Update Entry", use_container_width=True):
                jid, cid, lid = int(journal_id), int(case_id), int(lawyer_id)
                if not rec_exists("get_journal_by_id", "@Journal_id", jid):
                    st.error("❌ Journal ID does not exist.")
                elif not rec_exists("get_case_by_id", "@Case_id", cid):
                    st.error("❌ Case ID does not exist.")
                elif not rec_exists("get_lawyer_by_id", "@Lawyer_id", lid):
                    st.error("❌ Lawyer ID does not exist.")
                elif not lawyer_in_case(cid, lid):
                    st.error("❌ This lawyer is not assigned to this case.")
                elif not is_valid_name(entry_type):
                    st.error("❌ Entry Type must contain only letters and spaces.")
                elif content.strip() == "":
                    st.error("❌ Content cannot be empty.")
                else:
                    write_proc("EXEC update_journal_entry @Journal_id=?,@Case_id=?,@Lawyer_id=?,@Entry_date=?,@Entry_type=?,@Content=?",
                               (jid, cid, lid, entry_date.isoformat(), entry_type, content))
                    st.success("✅ Journal entry updated successfully!")

    with tab5:
        st.markdown("#### Delete a Journal Entry")
        st.warning("⚠️ This action is permanent.")
        with st.form("jn_del"):
            journal_id = st.number_input("Journal ID to Delete", min_value=1, step=1)
            if st.form_submit_button("🗑️ Delete Entry", use_container_width=True, type="primary"):
                jid = int(journal_id)
                if not rec_exists("get_journal_by_id", "@Journal_id", jid):
                    st.error("❌ Journal ID does not exist.")
                else:
                    write_proc("EXEC delete_journal_entry @Journal_id=?", (jid,))
                    st.success("✅ Journal entry deleted successfully!")


# Evidence Page 
def evidence_page():
    page_header("🔍", "Evidence Management",
                "Store and manage evidence linked to each case — documents, videos, digital files, etc.")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["➕ Add Evidence", "📋 View All", "🔍 For Case", "✏️ Update", "🗑️ Delete"]
    )

    with tab1:
        st.markdown("#### Add New Evidence")
        with st.form("ev_add"):
            c1, c2 = st.columns(2)
            evidence_id   = c1.number_input("Evidence ID", min_value=1, step=1)
            case_id       = c2.number_input("Case ID", min_value=1, step=1)
            c3, c4 = st.columns(2)
            title         = c3.text_input("Evidence Title", placeholder="e.g. Land Papers")
            evidence_type = c4.text_input("Evidence Type", placeholder="e.g. Document")
            description   = st.text_area("Description", placeholder="Short description of the evidence")
            c5, c6 = st.columns(2)
            submitted_date = c5.date_input("Submitted Date")
            file_path      = c6.text_input("File Path", placeholder="e.g. C:\\Evidence\\land.pdf")

            if st.form_submit_button("✅ Add Evidence", use_container_width=True):
                eid, cid = int(evidence_id), int(case_id)
                if rec_exists("get_evidence_by_id", "@Evidence_id", eid):
                    st.error("❌ Evidence ID already exists.")
                elif not rec_exists("get_case_by_id", "@Case_id", cid):
                    st.error("❌ Case ID does not exist.")
                elif title.strip() == "":
                    st.error("❌ Evidence Title cannot be empty.")
                elif rec_exists("get_evidence_by_title", "@Title", title):
                    st.error("❌ Evidence with this title already exists.")
                elif not is_valid_name(evidence_type):
                    st.error("❌ Evidence Type must contain only letters and spaces.")
                else:
                    write_proc("EXEC add_evidence @Evidence_id=?,@Case_id=?,@Title=?,@Evidence_type=?,@Description=?,@Submitted_date=?,@File_path=?",
                               (eid, cid, title, evidence_type, description, submitted_date.isoformat(), file_path))
                    st.success("✅ Evidence added successfully!")

    with tab2:
        st.markdown("#### All Evidence in Database")
        if st.button("📋 Load All Evidence", use_container_width=True):
            show_table(read_proc("EXEC get_all_evidence"), "Evidence")

    with tab3:
        st.markdown("#### Evidence for a Specific Case")
        cid = int(st.number_input("Case ID", min_value=1, step=1, key="ev_case"))
        if st.button("🔍 Get Evidence", use_container_width=True):
            if not rec_exists("get_case_by_id", "@Case_id", cid):
                st.error("❌ Case ID does not exist.")
            else:
                show_table(read_proc("EXEC get_evidence_for_case @Case_id=?", (cid,)), "Evidence")

    with tab4:
        st.markdown("#### Update an Evidence Record")
        with st.form("ev_upd"):
            c1, c2 = st.columns(2)
            evidence_id   = c1.number_input("Evidence ID to Update", min_value=1, step=1)
            case_id       = c2.number_input("New Case ID", min_value=1, step=1)
            c3, c4 = st.columns(2)
            title         = c3.text_input("New Evidence Title")
            evidence_type = c4.text_input("New Evidence Type")
            description   = st.text_area("New Description")
            c5, c6 = st.columns(2)
            submitted_date = c5.date_input("New Submitted Date")
            file_path      = c6.text_input("New File Path")

            if st.form_submit_button("✏️ Update Evidence", use_container_width=True):
                eid, cid = int(evidence_id), int(case_id)
                if not rec_exists("get_evidence_by_id", "@Evidence_id", eid):
                    st.error("❌ Evidence ID does not exist.")
                elif not rec_exists("get_case_by_id", "@Case_id", cid):
                    st.error("❌ Case ID does not exist.")
                elif title.strip() == "":
                    st.error("❌ Evidence Title cannot be empty.")
                elif not is_valid_name(evidence_type):
                    st.error("❌ Evidence Type must contain only letters and spaces.")
                else:
                    write_proc("EXEC update_evidence @Evidence_id=?,@Case_id=?,@Title=?,@Evidence_type=?,@Description=?,@Submitted_date=?,@File_path=?",
                               (eid, cid, title, evidence_type, description, submitted_date.isoformat(), file_path))
                    st.success("✅ Evidence updated successfully!")

    with tab5:
        st.markdown("#### Delete an Evidence Record")
        st.warning("⚠️ This action is permanent.")
        with st.form("ev_del"):
            evidence_id = st.number_input("Evidence ID to Delete", min_value=1, step=1)
            if st.form_submit_button("🗑️ Delete Evidence", use_container_width=True, type="primary"):
                eid = int(evidence_id)
                if not rec_exists("get_evidence_by_id", "@Evidence_id", eid):
                    st.error("❌ Evidence ID does not exist.")
                else:
                    write_proc("EXEC delete_evidence @Evidence_id=?", (eid,))
                    st.success("✅ Evidence deleted successfully!")


# Payment Page 
def payment_page():
    page_header("💰", "Payment Management",
                "Track all payments made by clients to lawyers. Lawyer and client must both be linked to the case.")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "➕ Add", "📋 View All", "🔍 For Case",
        "✏️ Update", "🔄 Update Status", "🗑️ Delete", "📊 Total Paid"
    ])

    with tab1:
        st.markdown("#### Add a New Payment")
        with st.form("pay_add"):
            c1, c2 = st.columns(2)
            payment_id = c1.number_input("Payment ID", min_value=1, step=1)
            case_id    = c2.number_input("Case ID", min_value=1, step=1)
            c3, c4 = st.columns(2)
            lawyer_id = c3.number_input("Lawyer ID", min_value=1, step=1, help="Must be assigned to this case")
            client_id = c4.number_input("Client ID", min_value=1, step=1, help="Must belong to this case")
            c5, c6, c7 = st.columns(3)
            amount       = c5.number_input("Amount (PKR)", min_value=0.01, step=500.0, format="%.2f")
            payment_date = c6.date_input("Payment Date")
            status       = c7.selectbox("Status", ["Paid", "Pending"])
            description  = st.text_area("Description / Remarks", placeholder="e.g. Initial legal fee")

            if st.form_submit_button("✅ Add Payment", use_container_width=True):
                pid, cid, lid, clid = int(payment_id), int(case_id), int(lawyer_id), int(client_id)
                if rec_exists("get_payment_by_id", "@Payment_id", pid):
                    st.error("❌ Payment ID already exists.")
                elif not rec_exists("get_case_by_id", "@Case_id", cid):
                    st.error("❌ Case ID does not exist.")
                elif not rec_exists("get_lawyer_by_id", "@Lawyer_id", lid):
                    st.error("❌ Lawyer ID does not exist.")
                elif not rec_exists("get_client_by_id", "@Client_id", clid):
                    st.error("❌ Client ID does not exist.")
                elif not lawyer_in_case(cid, lid):
                    st.error("❌ This lawyer is not assigned to this case.")
                elif not client_in_case(cid, clid):
                    st.error("❌ This client is not linked to this case.")
                elif not is_valid_amount(amount):
                    st.error("❌ Amount must be greater than 0.")
                else:
                    write_proc("EXEC add_payment @Payment_id=?,@Case_id=?,@Lawyer_id=?,@Client_id=?,@Amount=?,@Payment_date=?,@Status=?,@Description=?",
                               (pid, cid, lid, clid, amount, payment_date.isoformat(), status, description))
                    st.success("✅ Payment added successfully!")

    with tab2:
        st.markdown("#### All Payments in Database")
        if st.button("📋 Load All Payments", use_container_width=True):
            show_table(read_proc("EXEC get_all_payments"), "Payment")

    with tab3:
        st.markdown("#### Payments for a Specific Case")
        cid = int(st.number_input("Case ID", min_value=1, step=1, key="pay_case"))
        if st.button("🔍 Get Payments", use_container_width=True):
            if not rec_exists("get_case_by_id", "@Case_id", cid):
                st.error("❌ Case ID does not exist.")
            else:
                show_table(read_proc("EXEC get_payments_for_case @Case_id=?", (cid,)), "Payment")

    with tab4:
        st.markdown("#### Update a Payment")
        with st.form("pay_upd"):
            c1, c2 = st.columns(2)
            payment_id = c1.number_input("Payment ID to Update", min_value=1, step=1)
            case_id    = c2.number_input("New Case ID", min_value=1, step=1)
            c3, c4 = st.columns(2)
            lawyer_id = c3.number_input("New Lawyer ID", min_value=1, step=1)
            client_id = c4.number_input("New Client ID", min_value=1, step=1)
            c5, c6, c7 = st.columns(3)
            amount       = c5.number_input("New Amount (PKR)", min_value=0.01, step=500.0, format="%.2f")
            payment_date = c6.date_input("New Payment Date")
            status       = c7.selectbox("New Status", ["Paid", "Pending"])
            description  = st.text_area("New Description")

            if st.form_submit_button("✏️ Update Payment", use_container_width=True):
                pid, cid, lid, clid = int(payment_id), int(case_id), int(lawyer_id), int(client_id)
                if not rec_exists("get_payment_by_id", "@Payment_id", pid):
                    st.error("❌ Payment ID does not exist.")
                elif not rec_exists("get_case_by_id", "@Case_id", cid):
                    st.error("❌ Case ID does not exist.")
                elif not rec_exists("get_lawyer_by_id", "@Lawyer_id", lid):
                    st.error("❌ Lawyer ID does not exist.")
                elif not rec_exists("get_client_by_id", "@Client_id", clid):
                    st.error("❌ Client ID does not exist.")
                elif not lawyer_in_case(cid, lid):
                    st.error("❌ This lawyer is not assigned to this case.")
                elif not client_in_case(cid, clid):
                    st.error("❌ This client is not linked to this case.")
                elif not is_valid_amount(amount):
                    st.error("❌ Amount must be greater than 0.")
                else:
                    write_proc("EXEC update_payment @Payment_id=?,@Case_id=?,@Lawyer_id=?,@Client_id=?,@Amount=?,@Payment_date=?,@Status=?,@Description=?",
                               (pid, cid, lid, clid, amount, payment_date.isoformat(), status, description))
                    st.success("✅ Payment updated successfully!")

    with tab5:
        st.markdown("#### Update Payment Status Only")
        st.caption("Quickly mark a payment as Paid or Pending without changing other details.")
        with st.form("pay_st"):
            c1, c2 = st.columns(2)
            payment_id = c1.number_input("Payment ID", min_value=1, step=1)
            new_status = c2.selectbox("New Status", ["Paid", "Pending"])
            if st.form_submit_button("🔄 Update Status", use_container_width=True):
                pid = int(payment_id)
                if not rec_exists("get_payment_by_id", "@Payment_id", pid):
                    st.error("❌ Payment ID does not exist.")
                else:
                    write_proc("EXEC update_payment_status @Payment_id=?,@Status=?", (pid, new_status))
                    st.success("✅ Payment status updated successfully!")

    with tab6:
        st.markdown("#### Delete a Payment")
        st.warning("⚠️ This action is permanent.")
        with st.form("pay_del"):
            payment_id = st.number_input("Payment ID to Delete", min_value=1, step=1)
            if st.form_submit_button("🗑️ Delete Payment", use_container_width=True, type="primary"):
                pid = int(payment_id)
                if not rec_exists("get_payment_by_id", "@Payment_id", pid):
                    st.error("❌ Payment ID does not exist.")
                else:
                    write_proc("EXEC delete_payment @Payment_id=?", (pid,))
                    st.success("✅ Payment deleted successfully!")

    with tab7:
        st.markdown("#### Total Paid Amount for a Case")
        st.caption("Shows the sum of all payments with status 'Paid' for the selected case.")
        cid = int(st.number_input("Case ID", min_value=1, step=1, key="pay_total"))
        if st.button("📊 Calculate Total", use_container_width=True):
            if not rec_exists("get_case_by_id", "@Case_id", cid):
                st.error("❌ Case ID does not exist.")
            else:
                rows = read_proc("EXEC get_total_paid_amount @Case_id=?", (cid,))
                if rows:
                    st.metric(label=f"Total Paid for Case {cid}", value=f"PKR {rows[0][0]:,.2f}")


# Main App
def main():
    # Sidebar
    st.sidebar.title("⚖️ Law Firm")
    st.sidebar.caption("Management System")
    st.sidebar.divider()
    st.sidebar.markdown("**Navigate to a Module:**")

    page = st.sidebar.radio("Select a Module", [
        "🏠 Home / Dashboard",
        "⚖️ Judge",
        "👤 Client",
        "👨‍💼 Lawyer",
        "📁 Case",
        "🔗 Case-Lawyer",
        "🕐 Timeline",
        "📓 Journal",
        "🔍 Evidence",
        "💰 Payment",
    ])

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Project Info**")
    st.sidebar.caption("Course: Database Systems Lab")
    st.sidebar.caption("Subject: SQL + Python")
    st.sidebar.caption("Tool: Streamlit + SQL Server")

    # Page routing
    routes = {
        "🏠 Home / Dashboard": home_page,
        "⚖️ Judge":            judge_page,
        "👤 Client":           client_page,
        "👨‍💼 Lawyer":           lawyer_page,
        "📁 Case":             case_page,
        "🔗 Case-Lawyer":      case_lawyer_page,
        "🕐 Timeline":         timeline_page,
        "📓 Journal":          journal_page,
        "🔍 Evidence":         evidence_page,
        "💰 Payment":          payment_page,
    }
    routes[page]()


main()
