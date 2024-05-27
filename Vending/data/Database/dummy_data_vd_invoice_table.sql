-- Create a temporary table to generate numbers from 1 to 20
CREATE TEMPORARY TABLE IF NOT EXISTS numbers (n INT);

-- Insert numbers from 1 to 20
INSERT INTO numbers (n) VALUES (1),(2),(3),(4),(5),(6),(7),(8),(9),(10),
                                (11),(12),(13),(14),(15),(16),(17),(18),(19),(20);

-- Generate dummy data for vending machine IDs 1 to 5
INSERT INTO invoice (vd_invoice_vending_machine_id, vd_invoice_product_id, vd_invoice_date, vd_invoice_time, vd_invoice_payment_id)
SELECT
    machine_id,
    FLOOR(RAND() * 10) + 1 AS product_id, -- Random product ID between 1 and 10
    DATE_ADD('2024-01-01', INTERVAL FLOOR(RAND() * DATEDIFF(CURDATE(), '2024-01-01')) DAY) AS invoice_date, -- Random date within a range up to today's date
    SEC_TO_TIME(FLOOR(RAND() * 86400)) AS invoice_time, -- Random time (in seconds) converted to TIME
    IF(n % 2 = 1, 1, 2) AS payment_id -- Alternating payment IDs (1 and 2)
FROM
    numbers
CROSS JOIN (
    SELECT 1 AS machine_id UNION ALL
    SELECT 2 UNION ALL
    SELECT 3 UNION ALL
    SELECT 4 UNION ALL
    SELECT 5
) AS machines
ORDER BY invoice_date, invoice_time; -- Order the results by invoice_date and invoice_time in ascending order

-- Drop the temporary table
DROP TEMPORARY TABLE IF EXISTS numbers;
