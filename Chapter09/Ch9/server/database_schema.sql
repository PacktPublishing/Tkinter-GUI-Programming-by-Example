create table users (username text, real_name text);

create table relationship (user_one text, user_two text, blocked integer);

-- create a messages table per contact
-- message, author, order -> ? sqlite internal id