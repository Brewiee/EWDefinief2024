CREATE TABLE IF NOT EXISTS users.usertype (
    usertype_id INT AUTO_INCREMENT PRIMARY KEY,
    usertype_name VARCHAR(255) UNIQUE
);


CREATE TABLE IF NOT EXISTS users.userinfo (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    password_salt VARCHAR(255),
    perm_vend INT,
    perm_rest INT,
    perm_cr INT,
    perm_super INT,
    FOREIGN KEY (perm_vend) REFERENCES users.usertype(usertype_id),
    FOREIGN KEY (perm_rest) REFERENCES users.usertype(usertype_id),
    FOREIGN KEY (perm_cr) REFERENCES users.usertype(usertype_id),
    FOREIGN KEY (perm_super) REFERENCES users.usertype(usertype_id)
);
