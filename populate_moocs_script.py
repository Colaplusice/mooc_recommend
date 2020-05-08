# 添加和读取数据到数据库中
import os
import random

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mooc.settings")

django.setup()
from user.models import Mooc, Tags

Mooc.objects.all().delete()
Tags.objects.all().delete()
opener = open('moocs.csv', 'r')
opener.readline()
import csv

reader = csv.reader(opener)
images = os.listdir('media/mooc_image')
for line in reader:
    # 编号, 标题,, 机构, 难度, 学时, 热度, 语言, 开课日期, 副标题, 学科
    # 13134, 自动驾驶汽车,, 多伦多大学, 难（高级）, 2
    # 个月, 热度
    # 518, 英语, 2
    # 月15日, 专项课程, 计算机
    seq = line[0]
    title = line[1]
    institute = line[3]
    hard = line[4]
    time = line[5]
    hot = line[6]
    print('hot', hot)
    hot = int(hot.split(' ')[-1].replace(',', ''))
    language = line[7]
    start_time = line[8]
    subheading = line[9]
    tags = line[9:]
    print(tags)
    mooc = Mooc.objects.create(sequence=seq, title=title, institute=institute, hard=hard, class_hour=time, hot=hot, language=language, start_time=start_time, subheading=subheading, pic=random.choice(images))
    for tag in tags:
        tag_obj, created = Tags.objects.get_or_create(name=tag)
        print('created', created)
        mooc.tags.add(tag_obj.id)
