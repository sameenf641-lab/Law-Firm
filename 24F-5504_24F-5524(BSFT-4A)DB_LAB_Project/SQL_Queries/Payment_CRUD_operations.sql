CREATE PROCEDURE add_payment
    @Payment_id INT,
    @Case_id INT,
    @Lawyer_id INT,
    @Client_id INT,
    @Amount DECIMAL(10,2),
    @Payment_date DATE,
    @Status VARCHAR(50),
    @Description VARCHAR(300)
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Payment
        WHERE Payment_id = @Payment_id
    )

    BEGIN

        PRINT 'Error: Payment ID already exists.';

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

    ELSE IF NOT EXISTS (
        SELECT *
        FROM Client
        WHERE Client_id = @Client_id
    )

    BEGIN

        PRINT 'Error: Client does not exist.';

    END

    ELSE

    BEGIN

        INSERT INTO Payment (
            Payment_id,
            Case_id,
            Lawyer_id,
            Client_id,
            Amount,
            Payment_date,
            Status,
            Description
        )

        VALUES (
            @Payment_id,
            @Case_id,
            @Lawyer_id,
            @Client_id,
            @Amount,
            @Payment_date,
            @Status,
            @Description
        );

        PRINT 'Payment added successfully.';

    END

END;
EXEC add_payment
    @Payment_id = 1,
    @Case_id = 1,
    @Lawyer_id = 1,
    @Client_id = 1,
    @Amount = 50000,
    @Payment_date = '2026-05-10',
    @Status = 'Paid',
    @Description = 'Initial legal fee';

CREATE PROCEDURE get_all_payments
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Payment
    )

    BEGIN

        SELECT *
        FROM Payment;

    END

    ELSE

    BEGIN

        PRINT 'No payments found.';

    END

END;
EXEC get_all_payments;

CREATE PROCEDURE get_payments_for_case
    @Case_id INT
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Payment
        WHERE Case_id = @Case_id
    )

    BEGIN

        SELECT *
        FROM Payment
        WHERE Case_id = @Case_id;

    END

    ELSE

    BEGIN

        PRINT 'Error: No payment found for this case.';

    END

END;
EXEC get_payments_for_case
    @Case_id = 1;

CREATE PROCEDURE update_payment
    @Payment_id INT,
    @Case_id INT,
    @Lawyer_id INT,
    @Client_id INT,
    @Amount DECIMAL(10,2),
    @Payment_date DATE,
    @Status VARCHAR(50),
    @Description VARCHAR(300)
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Payment
        WHERE Payment_id = @Payment_id
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

        ELSE IF NOT EXISTS (
            SELECT *
            FROM Client
            WHERE Client_id = @Client_id
        )

        BEGIN

            PRINT 'Error: Client does not exist.';

        END

        ELSE

        BEGIN

            UPDATE Payment
            SET
                Case_id = @Case_id,
                Lawyer_id = @Lawyer_id,
                Client_id = @Client_id,
                Amount = @Amount,
                Payment_date = @Payment_date,
                Status = @Status,
                Description = @Description
            WHERE Payment_id = @Payment_id;

            PRINT 'Payment updated successfully.';

        END

    END

    ELSE

    BEGIN

        PRINT 'Error: Payment does not exist.';

    END

END;
EXEC update_payment
    @Payment_id = 1,
    @Case_id = 1,
    @Lawyer_id = 1,
    @Client_id = 1,
    @Amount = 75000,
    @Payment_date = '2026-05-15',
    @Status = 'Pending',
    @Description = 'Updated legal fee payment';

CREATE PROCEDURE update_payment_status
    @Payment_id INT,
    @Status VARCHAR(50)
AS
BEGIN

    IF EXISTS (
        SELECT *
        FROM Payment
        WHERE Payment_id = @Payment_id
    )

    BEGIN

        UPDATE Payment
        SET
            Status = @Status
        WHERE Payment_id = @Payment_id;

        PRINT 'Payment status updated successfully.';

    END

    ELSE

    BEGIN

        PRINT 'Error: Payment does not exist.';

    END

END;
EXEC update_payment_status
    @Payment_id = 1,
    @Status = 'Paid';

ALTER PROCEDURE delete_payment
    @Payment_id INT
AS
BEGIN
    IF EXISTS (
        SELECT *
        FROM Payment
        WHERE Payment_id = @Payment_id
    )
    BEGIN
        DELETE FROM Payment
        WHERE Payment_id = @Payment_id;

        PRINT 'Payment deleted successfully.';
    END
    ELSE
    BEGIN
        PRINT 'Error: Payment does not exist.';
    END
END;
CREATE PROCEDURE get_total_paid_amount
    @Case_id INT
AS
BEGIN
    SELECT ISNULL(SUM(Amount), 0) AS Total_Paid_Amount
    FROM Payment
    WHERE Case_id = @Case_id
    AND Status = 'Paid';
END;
EXEC get_total_paid_amount
    @Case_id = 1;