from django.db import models
from django.db.models import Avg


class User(models.Model):
    username = models.CharField(max_length=32, unique=True, verbose_name="账号")
    password = models.CharField(max_length=32, verbose_name="密码")
    phone = models.CharField(max_length=32, verbose_name="手机号码")
    name = models.CharField(max_length=32, verbose_name="名字", unique=True)
    address = models.CharField(max_length=32, verbose_name="地址")
    email = models.EmailField(verbose_name="邮箱")

    class Meta:
        verbose_name_plural = "用户"
        verbose_name = "用户"

    def __str__(self):
        return self.name


class Tags(models.Model):
    name = models.CharField(max_length=32, verbose_name="标签", unique=True)

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"

    def __str__(self):
        return self.name


class Mooc(models.Model):
    sequence = models.IntegerField(verbose_name='编号')
    title = models.CharField(max_length=64, verbose_name='标题')
    institute = models.CharField(verbose_name='机构', max_length=128)
    hard = models.CharField(max_length=32, verbose_name='难度')
    class_hour = models.CharField(verbose_name='学时', max_length=32)
    hot = models.IntegerField(verbose_name='热度')
    language = models.CharField(verbose_name='语言', max_length=128)
    start_time = models.CharField(verbose_name='开课日期', max_length=128)
    subheading = models.CharField(verbose_name='副标题', max_length=128)
    tags = models.ManyToManyField(Tags, verbose_name='学科', blank=True)
    collect = models.ManyToManyField(User, verbose_name="收藏者", blank=True)
    sump = models.IntegerField(verbose_name="收藏人数", default=0)
    num = models.IntegerField(verbose_name="浏览量", default=0)
    pic = models.FileField(verbose_name="封面图片", max_length=64, upload_to='mooc_cover')

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = "课程"

    def __str__(self):
        return self.title


class Rate(models.Model):
    mooc = models.ForeignKey(
        Mooc, on_delete=models.CASCADE, blank=True, null=True, verbose_name="课程id"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="用户id",
    )
    mark = models.FloatField(verbose_name="评分")
    create_time = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)

    @property
    def avg_mark(self):
        average = Rate.objects.all().aggregate(Avg('mark'))['mark__avg']
        return average

    class Meta:
        verbose_name = "评分信息"
        verbose_name_plural = verbose_name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    content = models.CharField(max_length=64, verbose_name="内容")
    create_time = models.DateTimeField(auto_now_add=True)
    good = models.IntegerField(verbose_name="点赞", default=0)
    mooc = models.ForeignKey(Mooc, on_delete=models.CASCADE, verbose_name="课程")

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name


class Num(models.Model):
    users = models.IntegerField(verbose_name="用户数量", default=0)
    moocs = models.IntegerField(verbose_name="课程数量", default=0)
    comments = models.IntegerField(verbose_name="评论数量", default=0)
    rates = models.IntegerField(verbose_name="评分汇总", default=0)
    actions = models.IntegerField(verbose_name="活动汇总", default=0)
    message_boards = models.IntegerField(verbose_name="留言汇总", default=0)

    class Meta:
        verbose_name = "数据统计"
        verbose_name_plural = verbose_name
