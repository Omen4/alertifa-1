-- name: get-messages-from-channel-id
SELECT ch.id AS channel_id, 
    m.id AS message_id, 
    m.user_id AS user_id, 
    u.user_name AS user_name, 
    m.created_at AS created_at,
    m.body AS content
FROM messages AS m
JOIN conversation AS c
ON (m.id = c.message_id)
JOIN channels AS ch
ON (c.channel_id = ch.id)
JOIN users AS u
ON (m.user_id = u.id)
WHERE c.channel_id = :channel_id
ORDER BY created_at DESC
LIMIT 50;

-- name: create-message^
SELECT * FROM create_message(:channel_id, :user_id, :body);

-- name: update-message!
UPDATE messages
SET body = :body
WHERE id = :message_id;

-- name: delete-message^
SELECT * FROM delete_message(:message_id);

-- name: read-message^
SELECT ch.id AS channel_id,
    ch.name AS channel_name,
    u.id AS user_id,
    u.user_name AS user_name,
    m.created_at AS created_at,
    m.updated_at AS updated_at,
    m.body AS body
FROM messages AS m
JOIN conversations AS c
ON (m.id = c.message_id)
JOIN channels AS ch
ON (c.channel_id = ch.id)
JOIN users AS u
ON (u.id = m.user_id)
WHERE m.id = :message_id;