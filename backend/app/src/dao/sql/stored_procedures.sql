-- insert message
CREATE OR REPLACE function create_message(channel_id_ BIGINT, user_id_ BIGINT, body_ VARCHAR)
    RETURNS VOID
as $$
DECLARE
    msg_id BIGINT;
BEGIN
    INSERT INTO messages (user_id, body)
    VALUES (user_id_, body_)
    RETURNING id INTO msg_id;
    INSERT INTO conversations (message_id, channel_id)
    VALUES (msg_id, channel_id_);
END;
$$ LANGUAGE plpgsql;

-- delete message
CREATE OR REPLACE function delete_message(message_id_ BIGINT)
    returns VOID
as $$
DECLARE
    channel_id_ BIGINT;
BEGIN
    SELECT c.channel_id INTO channel_id_
    FROM messages as m
    JOIN conversations as c
    ON (m.id = c.message_id)
    WHERE m.id = message_id_;
    DELETE FROM conversations
    WHERE message_id = message_id_
        AND channel_id = channel_id_;
    DELETE FROM messages
    WHERE id = message_id_;
END;
$$ LANGUAGE plpgsql;



SELECT * 
FROM messages AS m
JOIN conversations AS c
ON (m.id = c.message_id)
JOIN permissions AS p
ON (m.user_id = p.user_id AND c.channel_id = p.channel_id)
WHERE p.user_id = 1 AND p.role_id > 2 AND p.role_id > (
    SELECT p.role_id AS target_role
    FROM messages AS m
    JOIN conversations AS c
    ON (m.id = c.message_id)
    JOIN permissions AS p
    ON (m.user_id = p.user_id AND c.channel_id = p.channel_id)
    WHERE m.id = 788065826515320886
);