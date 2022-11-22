#/usr/bin/env python
#-*- coding:utf-8 -*-

# shutil 文件/目录 拷贝，移动，删除

import shutil
from pathlib import Path
from shutil import copyfile, copyfileobj, copy, copy2, copytree


# copyfileobj 核心代码，操作文件对象，复制内容
# copyfile 判断文件是否相同
# copy copyfile 复制内容，copymode rwx 权限
# copy2 copyfile 复制内容, copystat rwx 权限、其他元数据
# copytree 拷贝目录


# 创建测试目录
def mkd():
    Path('a/b/c').mkdir(parents=True, exist_ok=True)
    (Path('a/b') / '1.py').touch()
    (Path('a/b') / '2.py').touch()
    for i in range(5):
        (Path('a') / f'test{i}').touch(exist_ok=True)


# mkd()

src = 'a/'
dst = 'dst/'


# 删除目录
# shutil.rmtree(dst, True)  # FileNotFoundError => ,ignore_errors=True 忽略目录不存在错误


# 拷贝时过滤
def fn(x, names):
    # s = set()
    # for name in names:
    #     if name.endswith('.py'):
    #         # print(name)
    #         s.add(name)
    # return s
    # return { name for name in names if name.endswith('.py') }
    return set(filter(lambda name: name.endswith('.py'), names))

# 拷贝目录
# copytree(src, dst, dirs_exist_ok=True)    # FileExistsError => ,dirs_exist_ok=True 强制覆盖已存在目录
# copytree(src, dst, dirs_exist_ok=True, ignore=fn)    # ignore 过滤函数
# print(*Path(dst).rglob('*'), sep='\n')



# 作业：
# 1.选择一个已存在目录，其下创建 a/b/c/d 子目录解构，每个子目录下随机生成50个普通文件，文件名随机4个小写字母构成
# 2.将 a 目录所有内容拷贝到 dst 目录下，拷贝的普通文件名开头必须是 x,y,z 的

# 解法1： 每层目录下创建20随机文件，创建完随机文件不再创建，递归拷贝到 dst
import string, random, re
ALPHABET = string.ascii_lowercase

def filename(n):
    return "".join(random.choices(ALPHABET, k=n))

def exist_dir(dir):
    if not dir.exists():
        dir.mkdir()
    return dir

def file_manager(n=20):
    current_dir = exist_dir(Path('tmp'))
    exist_dir(current_dir / ('a/b/c/d'))
    src_dir = exist_dir(current_dir / 'a')
    dst_dir = exist_dir(current_dir / 'dst')

    def _to_touch(dir):
        for file in dir.iterdir():
            if file.is_dir() and file != dst_dir and len(list(file.glob('*'))) < n:
                for i in range(n):
                    (file / filename(4)).touch()
                _to_touch(file)

    _to_touch(current_dir)

    def _filter_file(src, names):
        return set(filter(lambda x: not re.match(r'^[xyz]', x), names))

    def _to_copy(src, dst):
        shutil.copytree(src, dst, dirs_exist_ok=True, ignore=_filter_file)
        # b,c 目录也会忽略，判断是目录进入 b,c 递归拷贝
        for file in src.iterdir():
            if file.is_dir():
                _to_copy(file, dst / (file.name))

    _to_copy(src_dir, dst_dir)

    def _del_file(dir):
        # print(*[ path for path in (Path('tmp').rglob('**/[a-z]*')) if not path.is_dir() ], sep='\n')
        fs = [path for path in dir.rglob('**/[a-z]*') if not path.is_dir()]
        for j in fs:
            j.unlink()
    # _del_file(dst_dir)

# file_manager()



# 解法2：在a目录下随机创建文件，每次运行删除重新创建拷贝，重点在忽略ignore_files函数
import shutil
from pathlib import Path
from string import ascii_lowercase
import random

# 创建目录
base = Path(__file__).parent / 'tmp'
shutil.rmtree(str(base))               # 创建之前删除一下已存在文件
sub = Path('a/b/c/d')
(base / sub).mkdir(parents=True, exist_ok=True)  # 路径，要求父目录存在不提示

# 随机递归在目录创建文件
# print(*sub.parents)
# print(list(sub.parents)[:-1])
dirs = [sub] + list(sub.parents)[:-1]  # 去掉最后的 .

# 创建文件
for i in range(50):
    name = "".join(random.choices(ascii_lowercase, k=4))
    (base / random.choice(dirs) / name).touch()

# 遍历所有文件, 解构
# print(*(base.rglob('*')), sep='\n')

# ignore 文件集合  -- 重点，排除目录
head = set('xyz')
def ignore_files(src, names):
    # print(src, type(src))      # 每层目录 str
    # print(names, type(names))  # 每层目录下的文件、目录列表 list
    return set(filter(lambda name: not name[0] in head and Path(src, name).is_file(), names))

# 拷贝到dst
shutil.copytree(str(base/'a'), str(base / 'dst'), ignore=ignore_files)