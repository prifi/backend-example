#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
@version:
author:fly
@time: 2021/03/09
@file: datetime.py
@function:
@modify:
"""
### datetime

# 处理日期和时间的标准库
from datetime import datetime, timedelta, timezone


# 获取当前时间（注意是时间类类型）
now = datetime.now()
utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)  # 获取当前UTC时间


# 格式化输出时间（注意是str类型）
df = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print('{:%Y/%m/%d %H:%M:%S}'.format(now))   # 使用 format 语法支持时间格式化打印


# str转换为datetime类
fday = datetime.strptime(df, '%Y-%m-%d %H:%M:%S')  # 注意是striptime


# 获取指定日期和时间
dt = datetime(2015, 4, 19, 12, 20)  # 使用指定日期创建datetime
dt = datetime(2015, 4, 19, 12, 20, tzinfo=timezone.utc)  # 指定时区


# datetime转换为timestamp
dtm = dt.timestamp()    # 1429446000.0 <class 'float'>


# timestamp转为datetime
t = 1429417200.0
datetime.fromtimestamp(t)     # 2015-04-19 04:20:00
datetime.fromtimestamp(1650412799, timezone(timedelta(hours=8)))   # 转换带时区的时间戳
datetime.fromtimestamp(1650369275, timezone.utc)   # utc时间戳转换
datetime.utcfromtimestamp(t)  # 转换成UTC时间


# datetime 加减
# 加减可以直接用+和-运算符，把datetime往后或往前计算，得到新的datetime（需要导入timedelta类）
old_time = now - timedelta(minutes=5)
new_time = now + timedelta(days=2, hours=12)  # 使用timedelta你可以很容易地算出前几天和后几天的时刻


# 本地时间设置时区 tzinfo 默认为None
tz_utc_8 = timezone(timedelta(hours=8))
d1 = datetime.strptime("2015-04-19 12:20:00", "%Y-%m-%d %H:%M:%S")
d2 = d1.replace(tzinfo=tz_utc_8)   # 设置北京时间时区
d3 = d2.astimezone(timezone.utc)   # 等同于：timezone(timedelta(hours=0))，可转换为任意时区
#--- 总结 ---
# 2015-04-19 12:20:00
# 2015-04-19 12:20:00+08:00   # replace：强制设置时区
# 2015-04-19 04:20:00+00:00   # asztime: 转换成其他时区时间


# 时区转换
# 利用 **带时区** 的datetime，通过astimezone()方法，可以转换到任意时区。
utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)    # 首先将本地时间转换为带时区的utc时间: UTC+0:00
bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))    # 转换为北京时间: UTC+8:00
tokyo_dt2 = bj_dt.astimezone(timezone(timedelta(hours=9))) # astimezone()将bj_dt转换时区为东京时间: UTC+9:00



#--- 总结 ---
# 时区转换的关键在于，拿到一个datetime时，要获知其正确的时区，然后强制设置时区，作为基准时间。
# 利用带时区的datetime，通过astimezone()方法，可以转换到任意时区。
# 存储datetime使用timestamp不受时区影响



## 练习：获取了用户输入的日期和时间如2015-1-21 9:01:30，以及一个时区信息如UTC+5:00，均是str，请编写一个函数将其转换为timestamp：
import re
from datetime import datetime, timedelta, timezone


def to_timestamp(dt_str, tz_str):
    try:
        t1 = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print('time eror')
        raise
    re_time = re.compile(r'.*?([\+\-\d]+).*')
    if not re_time.match(tz_str):
        return
    zone = int(re_time.match(tz_str).group(1))
    t = t1.replace(tzinfo=timezone(timedelta(hours=zone))).timestamp()
    return t
    # 方法2：一行代码搞定
    # return datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S').replace(
    #     tzinfo=timezone(timedelta(hours=int(re.match(r'.*?([\+\-\d]+).*', tz_str).group(1))))).timestamp()


# 测试:
t1 = to_timestamp('2015-6-1 08:10:30', 'UTC+7:00')
assert t1 == 1433121030.0, t1

t2 = to_timestamp('2015-5-31 16:10:30', 'UTC-09:00')
assert t2 == 1433121030.0, t2

print('ok')
