#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 文件IO

# r w a x
    # t b +

def w():
    # context
    # with 离开时，文件对象一定会调用close方法，不管是否正常执行
    with open('test', 'w+') as f:   # f为别名
        # f.write('aaa\n')
        # f.write('啊\n')
        # f.write('xyz\n')
        # f.write('ccc')
        # 逐行遍历
        f.write('\n'.join(map(str, range(101, 120))))
# w()

def r():
    with open('test', encoding='utf-8', mode='r+') as f2:
        for line in f2:
            # line_ft = line.strip().rpartition('/')[0]
            # print(line_ft)
            # 带换行符
            print(line.encode())
        # print(f2)  # 行迭代器

# 文本逐行处理，二进制方式处理多少字节
# f = open('test', encoding='utf-8', mode='r+')

# 上下文
## with f as f1:
# with f:
#     pass
# print(f.closed)

# print(f.read(3))
# print(f.read(1))
# print(f.read(1))
# print(f.seek(0,2))  # 跳到最后
# print(f.write(b'666'))
# print(f.tell())

# print(f.readline())
# f.seek(0)

# 一次性读取，以列表形式（不推荐）
# print(f.readlines())

# print(f.readline())

# 逐行读取 --> 推荐
# line = f.readline()
# while line:
#     print(line.strip())
#     line = f.readline()

# for line in open('test'):
#     print(line.strip())


# 使用map惰性写入
# print(f.writelines("\n".join(["444", "555"])))
# print(f.tell())
# f.writelines(map(lambda line: line+'\n', ['444', '555']))

# 文件描述符
# print(f.fileno())

# 关闭文件
# f.close()
# print(f.closed)




