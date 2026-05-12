CREATE PROCEDURE add_client
    @Client_id INT,
    @Name VARCHAR(100),
    @CNIC VARCHAR(20),
    @Phone_no VARCHAR(20),
    @Email VARCHAR(100),
    @Street VARCHAR(100),
    @City VARCHAR(100)
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Client
        WHERE Client_id = @Client_id
    )
    BEGIN
        PRINT 'Error: Client ID already exists.';
    END

    ELSE
    BEGIN
        INSERT INTO Client (
            Client_id,
            Name,
            CNIC,
            Phone_no,
            Email,
            Street,
            City
        )
        VALUES (
            @Client_id,
            @Name,
            @CNIC,
            @Phone_no,
            @Email,
            @Street,
            @City
        );

        PRINT 'Client added successfully.';
    END

END;
EXEC add_client
    @Client_id = 1,
    @Name = 'Ali Raza',
    @CNIC = '33100-1234567-1',
    @Phone_no = '03001234567',
    @Email = 'ali@gmail.com',
    @Street = 'Street 5',
    @City = 'Faisalabad';

CREATE PROCEDURE get_client_by_id
    @Client_id INT
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Client
        WHERE Client_id = @Client_id
    )

    BEGIN

        SELECT *
        FROM Client
        WHERE Client_id = @Client_id;

    END

    ELSE

    BEGIN

        PRINT 'Error: Client does not exist.';

    END

END;
EXEC get_client_by_id
    @Client_id = 1;

CREATE PROCEDURE update_client
    @Client_id INT,
    @Name VARCHAR(100),
    @Phone_no VARCHAR(20),
    @Street VARCHAR(100),
    @City VARCHAR(100)
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Client
        WHERE Client_id = @Client_id
    )

    BEGIN

        UPDATE Client
        SET
            Name = @Name,
            Phone_no = @Phone_no,
            Street = @Street,
            City = @City
        WHERE Client_id = @Client_id;

        PRINT 'Client updated successfully.';

    END

    ELSE

    BEGIN

        PRINT 'Error: Client does not exist.';

    END

END;
EXEC update_client
    @Client_id = 1,
    @Name = 'Ali Hassan',
    @Phone_no = '03111234567',
    @Street = 'Street 10',
    @City = 'Lahore';

ALTER PROCEDURE delete_client
    @Client_id INT
AS
BEGIN
    IF NOT EXISTS (
        SELECT *
        FROM Client
        WHERE Client_id = @Client_id
    )
    BEGIN
        PRINT 'Error: Client does not exist.';
    END

    ELSE IF EXISTS (
        SELECT *
        FROM [Case]
        WHERE Client_id = @Client_id
    )
    BEGIN
        PRINT 'Error: Client cannot be deleted because this client has case records.';
    END

    ELSE
    BEGIN
        DELETE FROM Client
        WHERE Client_id = @Client_id;

        PRINT 'Client deleted successfully.';
    END
END;
EXEC delete_client
    @Client_id = 1;
