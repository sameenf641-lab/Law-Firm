CREATE PROCEDURE add_lawyer
    @Lawyer_id INT,
    @Name VARCHAR(100),
    @Specialization VARCHAR(100),
    @Phone_no VARCHAR(20),
    @Email VARCHAR(100),
    @Bar_number VARCHAR(50),
    @Hourly_rate DECIMAL(10,2)
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Lawyer
        WHERE Lawyer_id = @Lawyer_id
    )

    BEGIN

        PRINT 'Error: Lawyer ID already exists.';

    END

    ELSE

    BEGIN

        INSERT INTO Lawyer (
            Lawyer_id,
            Name,
            Email,
            Bar_number,
            Specialization,
            Phone_no,
            Hourly_rate
        )

        VALUES (
            @Lawyer_id,
            @Name,
            @Email,
            @Bar_number,
            @Specialization,
            @Phone_no,
            @Hourly_rate
        );

        PRINT 'Lawyer added successfully.';

    END

END;
EXEC add_lawyer
    @Lawyer_id = 1,
    @Name = 'Ali Raza',
    @Specialization = 'Criminal Law',
    @Phone_no = '03001234567',
    @Email = 'ali@law.com',
    @Bar_number = 'BAR101',
    @Hourly_rate = 5000;

CREATE PROCEDURE get_all_lawyers
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Lawyer
    )

    BEGIN

        SELECT *
        FROM Lawyer;

    END

    ELSE

    BEGIN

        PRINT 'No lawyers found.';

    END

END;
EXEC get_all_lawyers;

CREATE PROCEDURE get_lawyer_by_id
    @Lawyer_id INT
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Lawyer
        WHERE Lawyer_id = @Lawyer_id
    )

    BEGIN

        SELECT *
        FROM Lawyer
        WHERE Lawyer_id = @Lawyer_id;

    END

    ELSE

    BEGIN

        PRINT 'Error: Lawyer does not exist.';

    END

END;
EXEC get_lawyer_by_id
    @Lawyer_id = 1;

CREATE PROCEDURE update_lawyer
    @Lawyer_id INT,
    @Name VARCHAR(100),
    @Specialization VARCHAR(100),
    @Phone_no VARCHAR(20),
    @Email VARCHAR(100),
    @Bar_number VARCHAR(50),
    @Hourly_rate DECIMAL(10,2)
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Lawyer
        WHERE Lawyer_id = @Lawyer_id
    )

    BEGIN

        UPDATE Lawyer
        SET
            Name = @Name,
            Specialization = @Specialization,
            Phone_no = @Phone_no,
            Email = @Email,
            Bar_number = @Bar_number,
            Hourly_rate = @Hourly_rate
        WHERE Lawyer_id = @Lawyer_id;

        PRINT 'Lawyer updated successfully.';

    END

    ELSE

    BEGIN

        PRINT 'Error: Lawyer does not exist.';

    END

END;
EXEC update_lawyer
    @Lawyer_id = 1,
    @Name = 'Ali Hassan',
    @Specialization = 'Corporate Law',
    @Phone_no = '03111234567',
    @Email = 'alihassan@law.com',
    @Bar_number = 'BAR200',
    @Hourly_rate = 7000;

CREATE PROCEDURE delete_lawyer
    @Lawyer_id INT
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Lawyer
        WHERE Lawyer_id = @Lawyer_id
    )

    BEGIN

        IF EXISTS (
            SELECT *
            FROM Case_Lawyer
            WHERE Lawyer_id = @Lawyer_id
        )

        BEGIN

            PRINT 'Error: Lawyer cannot be deleted because related case records exist.';

        END

        ELSE

        BEGIN

            DELETE FROM Lawyer
            WHERE Lawyer_id = @Lawyer_id;

            PRINT 'Lawyer deleted successfully.';

        END

    END

    ELSE

    BEGIN

        PRINT 'Error: Lawyer does not exist.';

    END

END;
EXEC delete_lawyer
    @Lawyer_id = 1;

