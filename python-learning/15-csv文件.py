#!/usr/bin/env python
#-*- coding: utf-8 -*-

# csv 文件
    # ,分割的值

import csv

rows = [
    ('id', 'name', 'age', 'desc'),
    [1, 2, 3, 4],
    ('2', 'tom', 20, 'tom\' name'),
    {'3', 'jerry', 30, """tom"s, brother"""},
    'abcdefg',
    ((1,), 2, 'abc')
]

# 特殊文件写入时多打印一行换行处理
# with open('t1.csv', 'w', newline='') as f:
#     for line in rows:
#         # f.write(",".join(map(str, line)) + '\r\n')
#         print(",".join(map(str, line)), file=f, end='\r\n')


# "(1,)",2,abc 注意这种格式区别，

# 读 csv
with open('t1.csv', 'r', newline='') as f:
    reader = csv.reader(f)
    # x = next(reader)
    # print(type(x), x)
    for line in reader:
        print(type(line), line)

# 写 csv
with open('t2.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(rows[0])
    writer.writerows(rows[1:])#!/usr/bin/env python
#-*- coding: utf-8 -*-

# csv 文件
    # ,分割的值

import csv

rows = [
    ('id', 'name', 'age', 'desc'),
    [1, 2, 3, 4],
    ('2', 'tom', 20, 'tom\' name'),
    {'3', 'jerry', 30, """tom"s, brother"""},
    'abcdefg',
    ((1,), 2, 'abc')
]

# 特殊文件写入时多打印一行换行处理
# with open('t1.csv', 'w', newline='') as f:
#     for line in rows:
#         # f.write(",".join(map(str, line)) + '\r\n')
#         print(",".join(map(str, line)), file=f, end='\r\n')


# "(1,)",2,abc 注意这种格式区别，

# 读 csv
with open('t1.csv', 'r', newline='') as f:
    reader = csv.reader(f)
    # x = next(reader)
    # print(type(x), x)
    for line in reader:
        print(type(line), line)

# 写 csv
with open('t2.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(rows[0])
