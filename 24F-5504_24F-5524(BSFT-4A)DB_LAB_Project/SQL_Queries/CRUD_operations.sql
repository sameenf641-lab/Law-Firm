CREATE OR ALTER PROCEDURE add_judge
    @Judge_id INT,
    @Name VARCHAR(100),
    @Court_name VARCHAR(100),
    @Contact_info VARCHAR(200),
    @Specialization VARCHAR(100)
AS
BEGIN

  

    IF @Judge_id <= 0
    BEGIN
        PRINT 'Error: Judge ID must be greater than zero.';
        RETURN;
    END

    IF EXISTS (
        SELECT *
        FROM Judge
        WHERE Judge_id = @Judge_id
    )
    BEGIN
        PRINT 'Error: Judge ID already exists.';
        RETURN;
    END

    IF LEN(@Name) < 3
    BEGIN
        PRINT 'Error: Judge name is too short.';
        RETURN;
    END

    IF LEN(@Court_name) < 3
    BEGIN
        PRINT 'Error: Court name is invalid.';
        RETURN;
    END

    IF @Contact_info IS NULL
    BEGIN
        PRINT 'Error: Contact information is required.';
        RETURN;
    END

    IF @Specialization IS NULL
    BEGIN
        PRINT 'Error: Specialization is required.';
        RETURN;
    END


    INSERT INTO Judge (
        Judge_id,
        Name,
        Court_name,
        Contact_info,
        Specialization
    )
    VALUES (
        @Judge_id,
        @Name,
        @Court_name,
        @Contact_info,
        @Specialization
    );

    PRINT 'Judge added successfully.';

END;


CREATE OR ALTER PROCEDURE get_all_judges
AS
BEGIN

    IF NOT EXISTS (
        SELECT *
        FROM Judge
    )
    BEGIN
        PRINT 'No judges found.';
        RETURN;
    END

    SELECT *
    FROM Judge;

END;
EXEC get_all_judges;


CREATE PROCEDURE updatejudge
    @Judge_id INT,
    @Name VARCHAR(100),
    @Court_name VARCHAR(100),
    @Contact_info VARCHAR(200),
    @Specialization VARCHAR(100)
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Judge
        WHERE Judge_id = @Judge_id
    )

    BEGIN

        UPDATE Judge
        SET
            Name = @Name,
            Court_name = @Court_name,
            Contact_info = @Contact_info,
            Specialization = @Specialization
        WHERE Judge_id = @Judge_id;

        PRINT 'Judge updated successfully.';

    END

    ELSE

    BEGIN

        PRINT 'Error: Judge does not exist.';

    END

END;
EXEC updatejudge
    @Judge_id = 1,
    @Name = 'Justice Hamid',
    @Court_name = 'Lahore High Court',
    @Contact_info = 'judge@court.com',
    @Specialization = 'Criminal Law';


CREATE PROCEDURE delete_judge
    @Judge_id INT
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Judge
        WHERE Judge_id = @Judge_id
    )

    BEGIN

        DELETE FROM Judge
        WHERE Judge_id = @Judge_id;

        PRINT 'Judge deleted successfully.';

    END

    ELSE

    BEGIN

        PRINT 'Error: Judge does not exist.';

    END

END;
EXEC delete_judge
    @Judge_id = 1;