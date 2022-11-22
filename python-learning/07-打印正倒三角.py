#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
# 作业：打印正倒三角
12 11 10 9 8 7 6 5 4 3 2 1
   11 10 9 8 7 6 5 4 3 2 1
      10 9 8 7 6 5 4 3 2 1
         9 8 7 6 5 4 3 2 1
           8 7 6 5 4 3 2 1
             7 6 5 4 3 2 1
               6 5 4 3 2 1
                 5 4 3 2 1
                   4 3 2 1
                     3 2 1
                       2 1
                         1
--------------------------
                         1
                       2 1
                     3 2 1
                   4 3 2 1
                 5 4 3 2 1
               6 5 4 3 2 1
             7 6 5 4 3 2 1
           8 7 6 5 4 3 2 1
         9 8 7 6 5 4 3 2 1
      10 9 8 7 6 5 4 3 2 1
   11 10 9 8 7 6 5 4 3 2 1
12 11 10 9 8 7 6 5 4 3 2 1
'''



# 思路1：右对齐
def triangle_print(n, reverse=False):
    lst = []
    for i in range(1, n+1): # 1,13
        line_list = [ x for x in reversed(range(1, i+1)) ]  # 每行反转
        str_line = ' '.join(map(str,(line_list)))
        lst.append(str_line)

    # 居右打印，计算出宽度
    # print(str_line, type(str_line), len(str_line))

    res = lst if reverse else reversed(lst)
    for line in res:
        print('{:>{}}'.format(line, len(str_line)))



def triangle_print(n):
    for i in range(1, n+1):
        for j in range(n, 0, -1):
            if j >= i:
                print(j, end=' ')
        print()

def triangle_print(n):
    for i in range(1, n+1):
        for j in range(n, 0, -1):
            if j <= i:
                print(j, end=' ')
            else:
                # print(j, end=' ')
                pass
        print()


# 1.补空格
# 2.右对齐
# 3.切片法


# 正三角
def triangle_print(n):
    for i in range(1, n+1):
        for j in range(n, 0, -1):
            if j <= i:
                print(j, end=' ')
            else:
                # print(j, end=' ')
                print(len(str(j)) * ' ', end=' ')
        print()


# 倒三角
def triangle_print(n):
    for i in range(n, 0, -1):
        for j in range(n, 0, -1):
            if j<=i:
                print(j, end=' ')
            else:
                print(len(str(j)) * ' ', end=' ')
        print()


# 正三角 右对齐
def triangle_print(n):
    tail = " ".join(map(str, range(n, 0, -1)))
    length = len(tail)
    for i in range(1, n):
        # for j in range(i, 0, -1):
        #     print(j, end=' ')
        # print()
        # line = " ".join(str(i) for i in range(i, 0, -1))
        line = " ".join(map(str, range(i, 0, -1)))
        print('{:>{}}'.format(line, length))
    print(tail)


# 正三角 切片， 使用 tail 截取步长得到
def triangle_print(n):
    tail = " ".join(map(str, range(n, 0, -1)))
    length = len(tail)
    start = -1
    step = 2  # 跨域 10、100、1000时需要调整步长 +1
    # points = [10, 100, 1000]
    points = {10 ** i for i in range(1,5)}
    for i in range(1, n):
        line = tail[start:]
        if (i+1) in points:
            step += 1
        start -= step
        # print(step)
        print('{:>{}}'.format(line, length))
    print(tail)


# 倒三角 切片， 使用 tail 截取步长得到，关注点集中到空格  补空格
def triangle_print(n):
    tail = " ".join(map(str, range(n, 0, -1)))
    print(tail)
    for i,c in enumerate(tail):
        # print(i, c)
        if c == ' ':
            print(i * ' ', tail[i+1:])


# 正三角 切片 补空格
def triangle_print(n):
    tail = " ".join(map(str, range(n, 0, -1)))
    width = len(tail)
    for i in range(width):
        if tail[-i] == ' ':
            print('{:>{}}'.format(tail[-i:], width))
    print(tail)

# 倒三角切片
def triangle_print(n):
    tail = " ".join(map(str, range(n, 0, -1)))
    width = len(tail)
    print(tail)
    for i in range(width):
        if tail[i] == ' ':
            print('{:>{}}'.format(tail[i:], width))

triangle_print(12)


