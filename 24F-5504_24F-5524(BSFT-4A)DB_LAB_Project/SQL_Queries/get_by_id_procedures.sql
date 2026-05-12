CREATE OR ALTER PROCEDURE get_timeline_entry_by_id
    @Entry_id INT
AS
BEGIN
    SELECT * FROM Timeline WHERE Entry_id = @Entry_id
END;

CREATE OR ALTER PROCEDURE get_journal_by_id
    @Journal_id INT
AS
BEGIN
    SELECT * FROM Journal WHERE Journal_id = @Journal_id
END;

CREATE OR ALTER PROCEDURE get_evidence_by_id
    @Evidence_id INT
AS
BEGIN
    SELECT * FROM Evidence WHERE Evidence_id = @Evidence_id
END;

CREATE OR ALTER PROCEDURE get_payment_by_id
    @Payment_id INT
AS
BEGIN
    SELECT * FROM Payment WHERE Payment_id = @Payment_id
END;
