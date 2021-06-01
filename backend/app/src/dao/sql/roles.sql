-- name: get-role-by-id^
SELECT id AS role_id,
    name AS role_name
FROM roles
WHERE id = :role_id;