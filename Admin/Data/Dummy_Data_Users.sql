INSERT INTO users.usertype (usertype_id, usertype_name) VALUES (1, 'Geen');
INSERT INTO users.usertype (usertype_id, usertype_name) VALUES (2, 'Admin');
INSERT INTO users.usertype (usertype_id, usertype_name) VALUES (3, 'User');

INSERT INTO users.userinfo (user_id, username, password, password_salt, perm_vend, perm_rest, perm_cr, perm_super) VALUES  (1, 'super', '$2b$12$THN4COn3ws/8cbTHIadg2eCT2pyvTchzqmoq3Ya21PbZEoaL3c9Be',"b'$2b$12$THN4COn3ws/8cbTHIadg2e'", 2, 2, 2, 2);
INSERT INTO users.userinfo (user_id, username, password, password_salt, perm_vend, perm_rest, perm_cr, perm_super) VALUES  (2, 'b', '$2b$12$A7I1IajnEhai.mnZR05iOe6bbY5srbVjGXyXwc8vzKJGKA07mcD6S',"b'$2b$12$A7I1IajnEhai.mnZR05iOe'", 1, 2, 3, 3);
INSERT INTO users.userinfo (user_id, username, password, password_salt, perm_vend, perm_rest, perm_cr, perm_super) VALUES  (3, 'c', '$2b$12$A7I1IajnEhai.mnZR05iOeBgH3mtbCUPHsN8E.O1TgsmrDK44eYp2',"b'$2b$12$A7I1IajnEhai.mnZR05iOe'", 1, 2, 3, 3);
INSERT INTO users.userinfo (user_id, username, password, password_salt, perm_vend, perm_rest, perm_cr, perm_super) VALUES  (4, 'd', '$2b$12$A7I1IajnEhai.mnZR05iOe8GCYrln0f9TfzKZSCJ9Z8Ln0kKSl5fe',"b'$2b$12$A7I1IajnEhai.mnZR05iOe'", 1, 2, 3, 3);
INSERT INTO users.userinfo (user_id, username, password, password_salt, perm_vend, perm_rest, perm_cr, perm_super) VALUES  (5, 'aa', '$2b$12$sGgnXnAg1bK5mNSFhIVwkON6Yn3gr/nqTFkeRihtnYvK7fl9VT54K',"b'$2b$12$sGgnXnAg1bK5mNSFhIVwkO'", 2, 2, 3, 3);
INSERT INTO users.userinfo (user_id, username, password, password_salt, perm_vend, perm_rest, perm_cr, perm_super) VALUES  (6, 'joeri', '$2b$12$hqtqfkqOgaBcLMvDP17WP.l1HGZjJeAzV0nW0fVQxC0.qVvAHFk0S',"b'$2b$12$hqtqfkqOgaBcLMvDP17WP.'", 2, 1, 1, 1);
INSERT INTO users.userinfo (user_id, username, password, password_salt, perm_vend, perm_rest, perm_cr, perm_super) VALUES  (7, 'mehmet', '$2b$12$3S6ix1Ug/vDpX2k4/ClZ1Om3lDrq4E8Hrw821cd0i/vZpQ38RXT8a',"b'$2b$12$3S6ix1Ug/vDpX2k4/ClZ1O'", 1, 1, 2, 1);
INSERT INTO users.userinfo (user_id, username, password, password_salt, perm_vend, perm_rest, perm_cr, perm_super) VALUES  (8, 'test', '$2b$12$THN4COn3ws/8cbTHIadg2eCT2pyvTchzqmoq3Ya21PbZEoaL3c9Be',"b'$2b$12$THN4COn3ws/8cbTHIadg2e'", 1, 1, 1, 1);
