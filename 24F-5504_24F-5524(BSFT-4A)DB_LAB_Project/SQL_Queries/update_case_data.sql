USE master;

-- Update Case_no values from 'C101' format to plain numbers stored as VARCHAR
UPDATE [Case] SET Case_no = '101' WHERE Case_id = 1;
UPDATE [Case] SET Case_no = '102' WHERE Case_id = 2;
UPDATE [Case] SET Case_no = '103' WHERE Case_id = 3;
UPDATE [Case] SET Case_no = '104' WHERE Case_id = 4;
UPDATE [Case] SET Case_no = '105' WHERE Case_id = 5;
UPDATE [Case] SET Case_no = '106' WHERE Case_id = 6;
UPDATE [Case] SET Case_no = '107' WHERE Case_id = 7;
UPDATE [Case] SET Case_no = '108' WHERE Case_id = 8;
