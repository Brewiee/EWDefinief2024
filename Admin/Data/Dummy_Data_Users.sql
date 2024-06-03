INSERT INTO users.usertype (usertype_id, usertype_name) VALUES (1, 'Geen');
INSERT INTO users.usertype (usertype_id, usertype_name) VALUES (2, 'Admin');
INSERT INTO users.usertype (usertype_id, usertype_name) VALUES (3, 'User');

INSERT INTO users.userinfo (user_id, username, password, password_salt, perm_vend, perm_rest, perm_cr, perm_super) VALUES  (1, 'super', '$2b$12$THN4COn3ws/8cbTHIadg2eCT2pyvTchzqmoq3Ya21PbZEoaL3c9Be',"b'$2b$12$THN4COn3ws/8cbTHIadg2e'", 2, 2, 2, 2);
INSERT INTO users.userinfo (user_id, username, password, password_salt, perm_vend, perm_rest, perm_cr, perm_super) VALUES  (2, 'vasilism', '$2b$12$pTLWgQ.qLIRKduh6UG1y1exr2Ws.gX0DU3RK7GEprSRA2WM4Rr/7K',"b'$2b$12$pTLWgQ.qLIRKduh6UG1y1e'", 1, 2, 1, 1);
INSERT INTO users.userinfo (user_id, username, password, password_salt, perm_vend, perm_rest, perm_cr, perm_super) VALUES  (3, 'vasiliss', '$2b$12$7hszRTdzXg7UYkAxp/r6Eeh9ownaRVQPlOumV11RCus6M7W.UbLj2',"b'$2b$12$7hszRTdzXg7UYkAxp/r6Ee'", 1, 3, 1, 1);
INSERT INTO users.userinfo (user_id, username, password, password_salt, perm_vend, perm_rest, perm_cr, perm_super) VALUES  (4, 'joeri', '$2b$12$hqtqfkqOgaBcLMvDP17WP.l1HGZjJeAzV0nW0fVQxC0.qVvAHFk0S',"b'$2b$12$hqtqfkqOgaBcLMvDP17WP.'", 2, 1, 1, 1);
INSERT INTO users.userinfo (user_id, username, password, password_salt, perm_vend, perm_rest, perm_cr, perm_super) VALUES  (5, 'mehmet', '$2b$12$3S6ix1Ug/vDpX2k4/ClZ1Om3lDrq4E8Hrw821cd0i/vZpQ38RXT8a',"b'$2b$12$3S6ix1Ug/vDpX2k4/ClZ1O'", 1, 1, 2, 1);