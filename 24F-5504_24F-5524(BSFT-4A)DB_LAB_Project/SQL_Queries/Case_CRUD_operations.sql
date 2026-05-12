CREATE PROCEDURE add_case
    @Case_id INT,
    @Case_no VARCHAR(50),
    @Title VARCHAR(150),
    @Case_type VARCHAR(100),
    @Status VARCHAR(50),
    @Filed_date DATE,
    @Client_id INT,
    @Judge_id INT
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM [Case]
        WHERE Case_id = @Case_id
    )

    BEGIN

        PRINT 'Error: Case ID already exists.';

    END

    ELSE IF NOT EXISTS (
        SELECT *
        FROM Client
        WHERE Client_id = @Client_id
    )

    BEGIN

        PRINT 'Error: Client does not exist.';

    END

    ELSE IF NOT EXISTS (
        SELECT *
        FROM Judge
        WHERE Judge_id = @Judge_id
    )

    BEGIN

        PRINT 'Error: Judge does not exist.';

    END

    ELSE

    BEGIN

        INSERT INTO [Case] (
            Case_id,
            Case_no,
            Title,
            Case_type,
            Status,
            Filed_date,
            Client_id,
            Judge_id
        )

        VALUES (
            @Case_id,
            @Case_no,
            @Title,
            @Case_type,
            @Status,
            @Filed_date,
            @Client_id,
            @Judge_id
        );

        PRINT 'Case added successfully.';

    END

END;
EXEC add_case
    @Case_id = 1,
    @Case_no = 'C101',
    @Title = 'Property Dispute',
    @Case_type = 'Civil',
    @Status = 'Open',
    @Filed_date = '2026-05-01',
    @Client_id = 1,
    @Judge_id = 1;

CREATE PROCEDURE get_all_cases
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM [Case]
    )

    BEGIN

        SELECT *
        FROM [Case];

    END

    ELSE

    BEGIN

        PRINT 'No cases found.';

    END

END;
EXEC get_all_cases;

CREATE PROCEDURE get_case_by_id
    @Case_id INT
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM [Case]
        WHERE Case_id = @Case_id
    )

    BEGIN

        SELECT *
        FROM [Case]
        WHERE Case_id = @Case_id;

    END

    ELSE

    BEGIN

        PRINT 'Error: Case does not exist.';

    END

END;
EXEC get_case_by_id
    @Case_id = 1;

CREATE PROCEDURE get_cases_by_client
    @Client_id INT
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM [Case]
        WHERE Client_id = @Client_id
    )

    BEGIN

        SELECT *
        FROM [Case]
        WHERE Client_id = @Client_id;

    END

    ELSE

    BEGIN

        PRINT 'Error: No case found for this client.';

    END

END;
EXEC get_cases_by_client
    @Client_id = 1;

CREATE PROCEDURE get_cases_by_status
    @Status VARCHAR(50)
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM [Case]
        WHERE Status = @Status
    )

    BEGIN

        SELECT *
        FROM [Case]
        WHERE Status = @Status;

    END

    ELSE

    BEGIN

        PRINT 'Error: No case found with this status.';

    END

END;
EXEC get_cases_by_status
    @Status = 'Open';

CREATE PROCEDURE update_case
    @Case_id INT,
    @Client_id INT,
    @Judge_id INT,
    @Title VARCHAR(150),
    @Status VARCHAR(50),
    @Filed_date DATE,
    @Case_no VARCHAR(50),
    @Case_type VARCHAR(100)
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM [Case]
        WHERE Case_id = @Case_id
    )

    BEGIN

        IF NOT EXISTS (
            SELECT *
            FROM Client
            WHERE Client_id = @Client_id
        )

        BEGIN

            PRINT 'Error: Client does not exist.';

        END

        ELSE IF NOT EXISTS (
            SELECT *
            FROM Judge
            WHERE Judge_id = @Judge_id
        )

        BEGIN

            PRINT 'Error: Judge does not exist.';

        END

        ELSE

        BEGIN

            UPDATE [Case]
            SET
                Client_id = @Client_id,
                Judge_id = @Judge_id,
                Title = @Title,
                Status = @Status,
                Filed_date = @Filed_date,
                Case_no = @Case_no,
                Case_type = @Case_type
            WHERE Case_id = @Case_id;

            PRINT 'Case updated successfully.';

        END

    END

    ELSE

    BEGIN

        PRINT 'Error: Case does not exist.';

    END

END;
EXEC update_case
    @Case_id = 1,
    @Client_id = 1,
    @Judge_id = 1,
    @Title = 'Updated Property Dispute',
    @Status = 'Pending',
    @Filed_date = '2026-05-10',
    @Case_no = 'C101',
    @Case_type = 'Civil';

CREATE PROCEDURE update_case_status
    @Case_id INT,
    @Status VARCHAR(50)
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM [Case]
        WHERE Case_id = @Case_id
    )

    BEGIN

        UPDATE [Case]
        SET
            Status = @Status
        WHERE Case_id = @Case_id;

        PRINT 'Case status updated successfully.';

    END

    ELSE

    BEGIN

        PRINT 'Error: Case does not exist.';

    END

END;
EXEC update_case_status
    @Case_id = 1,
    @Status = 'Closed';

CREATE PROCEDURE delete_case
    @Case_id INT
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM [Case]
        WHERE Case_id = @Case_id
    )

    BEGIN

        IF EXISTS (
            SELECT *
            FROM Case_Lawyer
            WHERE Case_id = @Case_id
        )

        BEGIN

            PRINT 'Error: Case cannot be deleted because related lawyer records exist.';

        END

        ELSE IF EXISTS (
            SELECT *
            FROM Timeline
            WHERE Case_id = @Case_id
        )

        BEGIN

            PRINT 'Error: Case cannot be deleted because timeline records exist.';

        END

        ELSE IF EXISTS (
            SELECT *
            FROM Journal
            WHERE Case_id = @Case_id
        )

        BEGIN

            PRINT 'Error: Case cannot be deleted because journal records exist.';

        END

        ELSE IF EXISTS (
            SELECT *
            FROM Evidence
            WHERE Case_id = @Case_id
        )

        BEGIN

            PRINT 'Error: Case cannot be deleted because evidence records exist.';

        END

        ELSE IF EXISTS (
            SELECT *
            FROM Payment
            WHERE Case_id = @Case_id
        )

        BEGIN

            PRINT 'Error: Case cannot be deleted because payment records exist.';

        END

        ELSE

        BEGIN

            DELETE FROM [Case]
            WHERE Case_id = @Case_id;

            PRINT 'Case deleted successfully.';

        END

    END

    ELSE

    BEGIN

        PRINT 'Error: Case does not exist.';

    END

END;
EXEC delete_case
    @Case_id = 1;

