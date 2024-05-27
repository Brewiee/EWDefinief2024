-- Generate dummy data for the inventory table
INSERT INTO inventory (vd_inventory_vending_machine_id, vd_inventory_product_id, vd_inventory_stock_quantity, vd_inventory_min_stock, vd_inventory_max_stock, vd_inventory_refill_stock)
SELECT
    machine_id AS vending_machine_id,
    product_id,
    FLOOR(RAND() * 100) + 1 AS stock_quantity, -- Random stock quantity between 1 and 100
    FLOOR(RAND() * 20) + 1 AS min_stock, -- Random min stock between 1 and 20
    FLOOR(RAND() * 100) + 21 AS max_stock, -- Random max stock between 21 and 120
    FLOOR(RAND() * 20) + 1 AS refill_stock -- Random refill stock between 1 and 20
FROM
(
    SELECT 
        machine_id,
        product_id
    FROM
    (
        SELECT 1 AS machine_id UNION ALL
        SELECT 2 UNION ALL
        SELECT 3 UNION ALL
        SELECT 4 UNION ALL
        SELECT 5
    ) AS machines
    CROSS JOIN
    (
        SELECT 1 AS product_id UNION ALL
        SELECT 2 UNION ALL
        SELECT 3 UNION ALL
        SELECT 4 UNION ALL
        SELECT 5 UNION ALL
        SELECT 6 UNION ALL
        SELECT 7 UNION ALL
        SELECT 8 UNION ALL
        SELECT 9 UNION ALL
        SELECT 10
    ) AS products
) AS vending_data;
