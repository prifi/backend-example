#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author:flybird 2022/08/01

class MenuItem(dict):
    """动态生成菜单"""

    def __init__(self, id, name, path=None):  # 自己本身是字典，给自己赋值
        super().__init__()
        self['id'] = id
        self['name'] = name
        self['path'] = path
        self['children'] = []

    # 实现获取children属性
    # 1.
    # def __getattr__(self, item):
    #     return self[item]

    # 2.
    # @property
    # def children(self):
    #     return self['children']

    # 3.
    def append(self, subitem):
        self['children'].append(subitem)
        return self

    # def __add__(self, other):
    #     self.append(other)

    __add__ = append


if __name__ == '__main__':
    menulist = []
    item = MenuItem(1, '用户管理')  # {'id': 1, 'name': '用户列表', 'path': None, 'children': []}
    # item.children.append(MenuItem(101, '用户列表'))
    # item.append(MenuItem(101, '用户列表'))
    item + MenuItem(101, '用户列表')
    menulist.append(item)
    print(menulist)
