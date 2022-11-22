-- 开始初始化数据;
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- 添加默认菜单
BEGIN;
INSERT INTO future.system_permissions (id, title, name, icon, sort, parent, type, component, alias, path, hidden, external_link, permission, cache, redirect) VALUES (1, '系统管理', '', 'form', 0, 0, 1, 'Layout', '', '/system', 0, 0, '', 0, '');
INSERT INTO future.system_permissions (id, title, name, icon, sort, parent, type, component, alias, path, hidden, external_link, permission, cache, redirect) VALUES (2, '用户管理', '', 'form', 0, 1, 1, 'system/user/index', '', '/system/user', 0, 0, '', 0, '');
INSERT INTO future.system_permissions (id, title, name, icon, sort, parent, type, component, alias, path, hidden, external_link, permission, cache, redirect) VALUES (3, '角色管理', '', 'form', 1, 1, 1, 'system/role/index', '', '/system/role', 0, 0, '', 0, '');
INSERT INTO future.system_permissions (id, title, name, icon, sort, parent, type, component, alias, path, hidden, external_link, permission, cache, redirect) VALUES (4, '权限管理', '', 'form', 2, 1, 1, 'system/permission/index', '', '/system/permission', 0, 0, '', 0, '');
INSERT INTO future.system_permissions (id, title, name, icon, sort, parent, type, component, alias, path, hidden, external_link, permission, cache, redirect) VALUES (9, '新建用户', '', '', 1, 2, 2, '', '', '', 1, 0, 'system:user:create', 0, '');
INSERT INTO future.system_permissions (id, title, name, icon, sort, parent, type, component, alias, path, hidden, external_link, permission, cache, redirect) VALUES (10, '用户列表', '', '', 0, 2, 2, '', '', '', 1, 0, 'system:user:list', 0, '');
INSERT INTO future.system_permissions (id, title, name, icon, sort, parent, type, component, alias, path, hidden, external_link, permission, cache, redirect) VALUES (11, '编辑用户', '', '', 2, 2, 2, '', '', '', 1, 0, 'system:user:edit', 0, '');
INSERT INTO future.system_permissions (id, title, name, icon, sort, parent, type, component, alias, path, hidden, external_link, permission, cache, redirect) VALUES (12, '删除用户', '', '', 3, 2, 2, '', '', '', 1, 0, 'system:user:delete', 0, '');
INSERT INTO future.system_permissions (id, title, name, icon, sort, parent, type, component, alias, path, hidden, external_link, permission, cache, redirect) VALUES (13, '角色列表', '', '', 0, 3, 2, '', '', '', 1, 0, 'system:role:list', 0, '');
INSERT INTO future.system_permissions (id, title, name, icon, sort, parent, type, component, alias, path, hidden, external_link, permission, cache, redirect) VALUES (14, '新建角色', '', '', 1, 3, 2, '', '', '', 1, 0, 'system:role:create', 0, '');
INSERT INTO future.system_permissions (id, title, name, icon, sort, parent, type, component, alias, path, hidden, external_link, permission, cache, redirect) VALUES (15, '编辑角色', '', '', 2, 3, 2, '', '', '', 1, 0, 'system:role:edit', 0, '');
INSERT INTO future.system_permissions (id, title, name, icon, sort, parent, type, component, alias, path, hidden, external_link, permission, cache, redirect) VALUES (16, '删除角色', '', '', 3, 3, 2, '', '', '', 1, 0, 'system:role:delete', 0, '');
INSERT INTO future.system_permissions (id, title, name, icon, sort, parent, type, component, alias, path, hidden, external_link, permission, cache, redirect) VALUES (17, '权限列表', '', '', 0, 4, 2, '', '', '', 1, 0, 'system:permission:list', 0, '');
INSERT INTO future.system_permissions (id, title, name, icon, sort, parent, type, component, alias, path, hidden, external_link, permission, cache, redirect) VALUES (18, '创建权限', '', '', 1, 4, 2, '', '', '', 1, 0, 'system:permission:create', 0, '');
INSERT INTO future.system_permissions (id, title, name, icon, sort, parent, type, component, alias, path, hidden, external_link, permission, cache, redirect) VALUES (19, '编辑权限', '', '', 2, 4, 2, '', '', '', 1, 0, 'system:permission:edit', 0, '');
INSERT INTO future.system_permissions (id, title, name, icon, sort, parent, type, component, alias, path, hidden, external_link, permission, cache, redirect) VALUES (20, '删除权限', '', '', 3, 4, 2, '', '', '', 1, 0, 'system:permission:delete', 0, '');
INSERT INTO future.system_permissions (id, title, name, icon, sort, parent, type, component, alias, path, hidden, external_link, permission, cache, redirect) VALUES (21, '编辑权限', '', '', 4, 3, 2, '', '', '', 1, 0, 'system:role:permission:edit', 0, '');

-- 添加默认用户
INSERT INTO `future`.`system_user` (`id`, `password`, `last_login`, `username`, `email`, `name`, `is_active`, `is_admin`, `create_date`, `update_date`) VALUES (1, 'pbkdf2_sha256$260000$qQO7Ra1iqjzfIe46nLbldV$1KGALmHAbktMDe6Zuqch8w06zYouu81S9nwiUTfh3cc=', NULL, 'lanyulei', 'lanyulei@c.com', 'lanyulei', 1, 1, '2021-05-31 04:48:43.872728', '2021-05-31 04:48:43.882163');

-- 添加默认角色
INSERT INTO `future`.`system_roles` (`id`, `name`, `remarks`) VALUES (1, '运维开发', '');

-- 添加默认用户与角色的关联
INSERT INTO `future`.`system_user_roles` (`id`, `user`, `role`) VALUES (1, 1, 1);

-- 添加默认角色的权限的关联
INSERT INTO future.system_role_permissions (id, role, permission) VALUES (1, 1, 1);
INSERT INTO future.system_role_permissions (id, role, permission) VALUES (3, 1, 2);
INSERT INTO future.system_role_permissions (id, role, permission) VALUES (4, 1, 3);
INSERT INTO future.system_role_permissions (id, role, permission) VALUES (7, 1, 4);
INSERT INTO future.system_role_permissions (id, role, permission) VALUES (8, 1, 9);
INSERT INTO future.system_role_permissions (id, role, permission) VALUES (20, 1, 10);
INSERT INTO future.system_role_permissions (id, role, permission) VALUES (22, 1, 11);
INSERT INTO future.system_role_permissions (id, role, permission) VALUES (24, 1, 12);
INSERT INTO future.system_role_permissions (id, role, permission) VALUES (25, 1, 13);
INSERT INTO future.system_role_permissions (id, role, permission) VALUES (26, 1, 14);
INSERT INTO future.system_role_permissions (id, role, permission) VALUES (28, 1, 15);
INSERT INTO future.system_role_permissions (id, role, permission) VALUES (29, 1, 16);
INSERT INTO future.system_role_permissions (id, role, permission) VALUES (30, 1, 17);
INSERT INTO future.system_role_permissions (id, role, permission) VALUES (32, 1, 18);
INSERT INTO future.system_role_permissions (id, role, permission) VALUES (33, 1, 19);
INSERT INTO future.system_role_permissions (id, role, permission) VALUES (34, 1, 20);
INSERT INTO future.system_role_permissions (id, role, permission) VALUES (35, 1, 21);
COMMIT;
