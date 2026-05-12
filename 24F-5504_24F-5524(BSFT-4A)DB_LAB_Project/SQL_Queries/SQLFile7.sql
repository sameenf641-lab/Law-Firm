CREATE PROCEDURE add_journal_entry
    @Journal_id INT,
    @Case_id INT,
    @Lawyer_id INT,
    @Entry_date DATE,
    @Entry_type VARCHAR(100),
    @Content VARCHAR(500)
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Journal
        WHERE Journal_id = @Journal_id
    )

    BEGIN

        PRINT 'Error: Journal ID already exists.';

    END

    ELSE IF NOT EXISTS (
        SELECT *
        FROM [Case]
        WHERE Case_id = @Case_id
    )

    BEGIN

        PRINT 'Error: Case does not exist.';

    END

    ELSE IF NOT EXISTS (
        SELECT *
        FROM Lawyer
        WHERE Lawyer_id = @Lawyer_id
    )

    BEGIN

        PRINT 'Error: Lawyer does not exist.';

    END

    ELSE

    BEGIN

        INSERT INTO Journal (
            Journal_id,
            Case_id,
            Lawyer_id,
            Entry_date,
            Entry_type,
            Content
        )

        VALUES (
            @Journal_id,
            @Case_id,
            @Lawyer_id,
            @Entry_date,
            @Entry_type,
            @Content
        );

        PRINT 'Journal entry added successfully.';

    END

END;
EXEC add_journal_entry
    @Journal_id = 1,
    @Case_id = 1,
    @Lawyer_id = 1,
    @Entry_date = '2026-05-10',
    @Entry_type = 'Case Notes',
    @Content = 'Client meeting completed successfully.';

CREATE PROCEDURE get_all_journals
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Journal
    )

    BEGIN

        SELECT *
        FROM Journal;

    END

    ELSE

    BEGIN

        PRINT 'No journal entries found.';

    END

END;
EXEC get_all_journals;

CREATE PROCEDURE get_journal_for_case
    @Case_id INT
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Journal
        WHERE Case_id = @Case_id
    )

    BEGIN

        SELECT *
        FROM Journal
        WHERE Case_id = @Case_id;

    END

    ELSE

    BEGIN

        PRINT 'Error: No journal found for this case.';

    END

END;
EXEC get_journal_for_case
    @Case_id = 1;

CREATE PROCEDURE update_journal_entry
    @Journal_id INT,
    @Case_id INT,
    @Lawyer_id INT,
    @Entry_date DATE,
    @Entry_type VARCHAR(100),
    @Content VARCHAR(500)
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Journal
        WHERE Journal_id = @Journal_id
    )

    BEGIN

        IF NOT EXISTS (
            SELECT *
            FROM [Case]
            WHERE Case_id = @Case_id
        )

        BEGIN

            PRINT 'Error: Case does not exist.';

        END

        ELSE IF NOT EXISTS (
            SELECT *
            FROM Lawyer
            WHERE Lawyer_id = @Lawyer_id
        )

        BEGIN

            PRINT 'Error: Lawyer does not exist.';

        END

        ELSE

        BEGIN

            UPDATE Journal
            SET
                Case_id = @Case_id,
                Lawyer_id = @Lawyer_id,
                Entry_date = @Entry_date,
                Entry_type = @Entry_type,
                Content = @Content
            WHERE Journal_id = @Journal_id;

            PRINT 'Journal entry updated successfully.';

        END

    END

    ELSE

    BEGIN

        PRINT 'Error: Journal entry does not exist.';

    END

END;
EXEC update_journal_entry
    @Journal_id = 1,
    @Case_id = 1,
    @Lawyer_id = 1,
    @Entry_date = '2026-05-15',
    @Entry_type = 'Updated Notes',
    @Content = 'Updated journal details.';

CREATE PROCEDURE delete_journal_entry
    @Journal_id INT
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Journal
        WHERE Journal_id = @Journal_id
    )

    BEGIN

        DELETE FROM Journal
        WHERE Journal_id = @Journal_id;

        PRINT 'Journal entry deleted successfully.';

    END

    ELSE

    BEGIN

        PRINT 'Error: Journal entry does not exist.';

    END

END;
EXEC delete_journal_entry
    @Journal_id = 1;

