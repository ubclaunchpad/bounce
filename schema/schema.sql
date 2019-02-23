CREATE TYPE member_role AS ENUM ('President', 'Admin', 'Member');

DROP TABLE IF EXISTS clubs CASCADE;
CREATE TABLE clubs (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    website_url TEXT,
    facebook_url TEXT,
    instagram_url TEXT,
    twitter_url TEXT,
    search_vector TSVECTOR,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT (now() at time zone 'utc')
);

DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    full_name TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    secret TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    bio TEXT NOT NULL,
    search_vector TSVECTOR,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT (now() at time zone 'utc')
);

DROP TABLE IF EXISTS memberships;
CREATE TABLE memberships (
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    club_id INT NOT NULL REFERENCES clubs(id) ON DELETE CASCADE,
    position TEXT NOT NULL,
    role member_role NOT NULL, 
    PRIMARY KEY (user_id, club_id),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT (now() at time zone 'utc')
);