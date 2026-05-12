CREATE PROCEDURE add_evidence
    @Evidence_id INT,
    @Case_id INT,
    @Title VARCHAR(150),
    @Evidence_type VARCHAR(100),
    @Description VARCHAR(500),
    @Submitted_date DATE,
    @File_path VARCHAR(300)
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Evidence
        WHERE Evidence_id = @Evidence_id
    )

    BEGIN

        PRINT 'Error: Evidence ID already exists.';

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

        INSERT INTO Evidence (
            Evidence_id,
            Case_id,
            Title,
            Evidence_type,
            Description,
            Submitted_date,
            File_path
        )

        VALUES (
            @Evidence_id,
            @Case_id,
            @Title,
            @Evidence_type,
            @Description,
            @Submitted_date,
            @File_path
        );

        PRINT 'Evidence added successfully.';

    END

END;
EXEC add_evidence
    @Evidence_id = 1,
    @Case_id = 1,
    @Title = 'Property Documents',
    @Evidence_type = 'Document',
    @Description = 'Original property ownership papers',
    @Submitted_date = '2026-05-10',
    @File_path = 'C:\Evidence\property.pdf';

CREATE PROCEDURE get_all_evidence
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Evidence
    )

    BEGIN

        SELECT *
        FROM Evidence;

    END

    ELSE

    BEGIN

        PRINT 'No evidence found.';

    END

END;
EXEC get_all_evidence;

CREATE PROCEDURE get_evidence_for_case
    @Case_id INT
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Evidence
        WHERE Case_id = @Case_id
    )

    BEGIN

        SELECT *
        FROM Evidence
        WHERE Case_id = @Case_id;

    END

    ELSE

    BEGIN

        PRINT 'Error: No evidence found for this case.';

    END

END;
EXEC get_evidence_for_case
    @Case_id = 1;

CREATE PROCEDURE update_evidence
    @Evidence_id INT,
    @Case_id INT,
    @Title VARCHAR(150),
    @Evidence_type VARCHAR(100),
    @Description VARCHAR(500),
    @Submitted_date DATE,
    @File_path VARCHAR(300)
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Evidence
        WHERE Evidence_id = @Evidence_id
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

            UPDATE Evidence
            SET
                Case_id = @Case_id,
                Title = @Title,
                Evidence_type = @Evidence_type,
                Description = @Description,
                Submitted_date = @Submitted_date,
                File_path = @File_path
            WHERE Evidence_id = @Evidence_id;

            PRINT 'Evidence updated successfully.';

        END

    END

    ELSE

    BEGIN

        PRINT 'Error: Evidence does not exist.';

    END

END;
EXEC update_evidence
    @Evidence_id = 1,
    @Case_id = 1,
    @Title = 'Updated Property Documents',
    @Evidence_type = 'PDF',
    @Description = 'Updated ownership papers',
    @Submitted_date = '2026-05-15',
    @File_path = 'C:\Evidence\updated_property.pdf';

ALTER PROCEDURE delete_evidence
    @Evidence_id INT
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Evidence
        WHERE Evidence_id = @Evidence_id
    )

    BEGIN

        DELETE FROM Evidence
        WHERE Evidence_id = @Evidence_id;

        PRINT 'Evidence deleted successfully.';

    END

    ELSE

    BEGIN

        PRINT 'Error: Evidence does not exist.';

    END

END;
EXEC delete_evidence
    @Evidence_id = 2;

