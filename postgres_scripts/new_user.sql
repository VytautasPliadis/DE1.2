-- Create a new user with a password
CREATE USER new_user WITH PASSWORD 'test_password';

-- Grant necessary permissions
GRANT CONNECT ON DATABASE postgres TO new_user;
GRANT USAGE ON SCHEMA public TO new_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO new_user;
ALTER DEFAULT PRIVILEGES FOR ROLE new_user IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO new_user;

-- Delete user
REVOKE ALL PRIVILEGES ON DATABASE postgres FROM new_user;
DROP USER test_user;

-- Show all users
SELECT usename FROM pg_user;