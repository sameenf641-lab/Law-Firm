ALTER PROCEDURE assign_lawyer_to_case
    @id INT,
    @Case_id INT,
    @Lawyer_id INT,
    @Assigned_date DATE,
    @Role VARCHAR(100)
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Case_Lawyer
        WHERE id = @id
    )
    BEGIN
        PRINT 'Error: Assignment ID already exists.';
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

    ELSE IF EXISTS (
        SELECT *
        FROM Case_Lawyer
        WHERE Case_id = @Case_id
        AND Lawyer_id = @Lawyer_id
    )
    BEGIN
        PRINT 'Error: This lawyer is already assigned to this case.';
    END

    ELSE
    BEGIN
        INSERT INTO Case_Lawyer (
            id,
            Case_id,
            Lawyer_id,
            Assigned_date,
            Role
        )
        VALUES (
            @id,
            @Case_id,
            @Lawyer_id,
            @Assigned_date,
            @Role
        );

        PRINT 'Lawyer assigned to case successfully.';
    END

END;
EXEC assign_lawyer_to_case
    @id = 2,
    @Case_id = 1,
    @Lawyer_id = 2,
    @Assigned_date = '2026-05-01',
    @Role = 'Assistant Lawyer';

CREATE PROCEDURE get_all_assignments
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Case_Lawyer
    )

    BEGIN

        SELECT *
        FROM Case_Lawyer;

    END

    ELSE

    BEGIN

        PRINT 'No case-lawyer assignments found.';

    END

END;
EXEC get_all_assignments;

CREATE PROCEDURE get_lawyers_for_case
    @Case_id INT
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Case_Lawyer
        WHERE Case_id = @Case_id
    )

    BEGIN

        SELECT *
        FROM Case_Lawyer
        WHERE Case_id = @Case_id;

    END

    ELSE

    BEGIN

        PRINT 'Error: No lawyer assigned to this case.';

    END

END;
EXEC get_lawyers_for_case
    @Case_id = 1;

ALTER PROCEDURE get_cases_for_lawyer
    @Lawyer_id INT
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Case_Lawyer
        WHERE Lawyer_id = @Lawyer_id
    )

    BEGIN

        SELECT *
        FROM Case_Lawyer
        WHERE Lawyer_id = @Lawyer_id;

    END

    ELSE

    BEGIN

        PRINT 'Error: No case found for this lawyer.';

    END

END;
EXEC get_cases_for_lawyer
    @Lawyer_id = 1;

CREATE PROCEDURE update_assignment
    @Old_Case_id INT,
    @Old_Lawyer_id INT,
    @New_Case_id INT,
    @New_Lawyer_id INT
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Case_Lawyer
        WHERE Case_id = @Old_Case_id
        AND Lawyer_id = @Old_Lawyer_id
    )

    BEGIN

        IF NOT EXISTS (
            SELECT *
            FROM [Case]
            WHERE Case_id = @New_Case_id
        )

        BEGIN

            PRINT 'Error: New case does not exist.';

        END

        ELSE IF NOT EXISTS (
            SELECT *
            FROM Lawyer
            WHERE Lawyer_id = @New_Lawyer_id
        )

        BEGIN

            PRINT 'Error: New lawyer does not exist.';

        END

        ELSE

        BEGIN

            UPDATE Case_Lawyer
            SET
                Case_id = @New_Case_id,
                Lawyer_id = @New_Lawyer_id
            WHERE Case_id = @Old_Case_id
            AND Lawyer_id = @Old_Lawyer_id;

            PRINT 'Case-lawyer assignment updated successfully.';

        END

    END

    ELSE

    BEGIN

        PRINT 'Error: Case-lawyer assignment does not exist.';

    END

END;
EXEC update_assignment
    @Old_Case_id = 1,
    @Old_Lawyer_id = 1,
    @New_Case_id = 2,
    @New_Lawyer_id = 2;

CREATE PROCEDURE delete_assignment
    @Case_id INT,
    @Lawyer_id INT
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Case_Lawyer
        WHERE Case_id = @Case_id
        AND Lawyer_id = @Lawyer_id
    )

    BEGIN

        DELETE FROM Case_Lawyer
        WHERE Case_id = @Case_id
        AND Lawyer_id = @Lawyer_id;

        PRINT 'Case-lawyer assignment deleted successfully.';

    END

    ELSE

    BEGIN

        PRINT 'Error: Case-lawyer assignment does not exist.';

    END

END;
EXEC delete_assignment
    @Case_id = 1,
    @Lawyer_id = 1;

CREATE PROCEDURE add_timeline_entry
    @Entry_id INT,
    @Case_id INT,
    @Hearing_date DATE,
    @Next_date DATE,
    @Proceeding_type VARCHAR(100),
    @Outcome VARCHAR(200),
    @Note VARCHAR(300)
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Timeline
        WHERE Entry_id = @Entry_id
    )

    BEGIN

        PRINT 'Error: Timeline ID already exists.';

    END

    ELSE IF NOT EXISTS (
        SELECT *
        FROM [Case]
        WHERE Case_id = @Case_id
    )

    BEGIN

        PRINT 'Error: Case does not exist.';

    END

    ELSE

    BEGIN

        INSERT INTO Timeline (
            Entry_id,
            Case_id,
            Hearing_date,
            Next_date,
            Proceeding_type,
            Outcome,
            Note
        )

        VALUES (
            @Entry_id,
            @Case_id,
            @Hearing_date,
            @Next_date,
            @Proceeding_type,
            @Outcome,
            @Note
        );

        PRINT 'Timeline entry added successfully.';

    END

END;
EXEC add_timeline_entry
    @Entry_id = 1,
    @Case_id = 1,
    @Hearing_date = '2026-05-10',
    @Next_date = '2026-05-20',
    @Proceeding_type = 'Hearing',
    @Outcome = 'Adjourned',
    @Note = 'Next hearing scheduled';

CREATE PROCEDURE get_all_timeline_entries
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Timeline
    )

    BEGIN

        SELECT *
        FROM Timeline;

    END

    ELSE

    BEGIN

        PRINT 'No timeline entries found.';

    END

END;
EXEC get_all_timeline_entries;

CREATE PROCEDURE get_timeline_for_case
    @Case_id INT
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Timeline
        WHERE Case_id = @Case_id
    )

    BEGIN

        SELECT *
        FROM Timeline
        WHERE Case_id = @Case_id
        ORDER BY Hearing_date;

    END

    ELSE

    BEGIN

        PRINT 'Error: No timeline found for this case.';

    END

END;
EXEC get_timeline_for_case
    @Case_id = 1;

CREATE PROCEDURE update_timeline_entry
    @Entry_id INT,
    @Case_id INT,
    @Hearing_date DATE,
    @Next_date DATE,
    @Proceeding_type VARCHAR(100),
    @Outcome VARCHAR(200),
    @Note VARCHAR(300)
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Timeline
        WHERE Entry_id = @Entry_id
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

        ELSE

        BEGIN

            UPDATE Timeline
            SET
                Case_id = @Case_id,
                Hearing_date = @Hearing_date,
                Next_date = @Next_date,
                Proceeding_type = @Proceeding_type,
                Outcome = @Outcome,
                Note = @Note
            WHERE Entry_id = @Entry_id;

            PRINT 'Timeline entry updated successfully.';

        END

    END

    ELSE

    BEGIN

        PRINT 'Error: Timeline entry does not exist.';

    END

END;
EXEC update_timeline_entry
    @Entry_id = 1,
    @Case_id = 1,
    @Hearing_date = '2026-05-15',
    @Next_date = '2026-05-25',
    @Proceeding_type = 'Final Hearing',
    @Outcome = 'Pending',
    @Note = 'Updated hearing details';

CREATE PROCEDURE delete_timeline_entry
    @Entry_id INT
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Timeline
        WHERE Entry_id = @Entry_id
    )

    BEGIN

        DELETE FROM Timeline
        WHERE Entry_id = @Entry_id;

        PRINT 'Timeline entry deleted successfully.';

    END

    ELSE

    BEGIN

        PRINT 'Error: Timeline entry does not exist.';

    END

END;
EXEC delete_timeline_entry
    @Entry_id = 1;

