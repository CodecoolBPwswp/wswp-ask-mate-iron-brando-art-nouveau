ALTER TABLE question
    ADD user_id integer;

ALTER TABLE question
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id);
