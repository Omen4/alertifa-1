-- name: get-channel-by-id^
SELECT id AS channel_id,
    name AS channel_name,
    created_at,
    updated_at
FROM channels
WHERE id = :channel_id;