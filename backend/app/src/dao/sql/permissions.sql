-- name: get-user-permissions-from-id
SELECT p.channel_id AS channel_id, 
    c.name AS channel_name,
    r.id AS role_id,
    r.name AS role_name
FROM permissions AS p
JOIN users AS u
ON (p.user_id = u.id)
JOIN roles AS r 
ON (p.role_id = r.id)
JOIN channels AS c
ON (c.id = p.channel_id)
WHERE p.user_id = :user_id;

-- name: check-permission^
SELECT p.channel_id AS channel_id, 
    c.name AS channel_name,
    r.id AS role_id,
    r.name AS role_name
FROM permissions AS p
JOIN users AS u
ON (p.user_id = u.id)
JOIN roles AS r 
ON (p.role_id = r.id)
JOIN channels AS c
ON (c.id = p.channel_id)
WHERE p.user_id = :user_id
    AND c.id = :channel_id
    AND p.role_id >= :minimum_role;

-- name: check-user-is-owner^
SELECT * 
FROM messages AS m
JOIN conversations AS c
ON (m.id = c.message_id)
JOIN permissions AS p
ON (c.channel_id = p.channel_id AND p.user_id = m.user_id)
WHERE m.user_id = :user_id AND m.id = :message_id;

-- name: check-permission-from-message-id^
SELECT * 
FROM messages AS m
JOIN conversations AS c
ON (m.id = c.message_id)
JOIN permissions AS p
ON (c.channel_id = p.channel_id AND p.user_id = m.user_id)
WHERE m.user_id = :user_id 
    AND m.id = :message_id
    AND p.role_id >= :role_id;

-- name: check-mod-privileges
SELECT * 
FROM permissions
WHERE channel_id = (
    SELECT c.channel_id
    FROM messages AS m
    JOIN conversations AS c
    ON (m.id = c.message_id)
    WHERE m.id = :message_id
) AND user_id = :user_id;

-- name: check-mod-permissions
SELECT * 
FROM permissions
WHERE channel_id = (
    SELECT c.channel_id
    FROM messages AS m
    JOIN conversations AS c
    ON (m.id = c.message_id)
    WHERE m.id = :message_id
) AND user_id = :user_id;

--name: get-user-permission^
SELECT role_id
FROM permissions
WHERE channel_id = :channel_id
    AND user_id = :user_id;

-- name: set-permission!
UPDATE permissions
SET role_id = :role_id
WHERE user_id = :user_id 
    AND channel_id = :channel_id;

-- name: create-permission!
INSERT INTO permissions(user_id, channel_id, role_id)
VALUES (:user_id, :channel_id, 0);