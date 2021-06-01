-- name: get-user-by-username^
SELECT id,
       user_name,
       email,
       salt,
       hashed_password,
       created_at,
       updated_at
FROM users
WHERE user_name = :user_name
LIMIT 1;

-- name: get-user-by-id^
SELECT id AS user_id,
       user_name,
       email,
       created_at,
       bio
FROM users
WHERE id = :user_id
LIMIT 1;

-- name: invalidate-previous-token<!
UPDATE users
SET jwt_id = jwt_id + 1
WHERE id = :user_id
    AND user_name = :user_name
    AND email = :email
    AND jwt_id = :jwt_id
RETURNING jwt_id;

-- name: check-user^
SELECT id AS user_id,
       user_name,
       email,
       salt,
       hashed_password,
       created_at,
       updated_at,
       jwt_id
FROM users
WHERE id = :user_id
    AND user_name = :user_name
    AND email = :email
    AND jwt_id = :jwt_id
LIMIT 1;

-- name: get-user-by-email^
SELECT id AS user_id,
       user_name,
       email,
       salt,
       hashed_password,
       created_at,
       updated_at,
       jwt_id
FROM users
WHERE email = :email
LIMIT 1;

-- name: create-user<!
INSERT INTO users (user_name, email, salt, hashed_password)
VALUES (:user_name, :email, :salt, :hashed_password)
RETURNING id AS user_id, user_name, email, jwt_id;

-- name: update-email!
UPDATE users 
SET email = :email
WHERE id = :user_id;

-- name: update-user-name!
UPDATE users 
SET user_name = :user_name
WHERE id = :user_id;

--name: update-password!
UPDATE users
SET hashed_password = :hashed_password,
    salt = :salt
WHERE id = :user_id;

--name: update-bio!
UPDATE users
SET bio = :bio
WHERE id = :user_id;
