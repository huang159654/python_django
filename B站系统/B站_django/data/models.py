from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserModel(AbstractUser):
    mobile = models.IntegerField(verbose_name='手机号码', default='13888888888')
    gender = models.IntegerField(verbose_name='性别', choices=((0, '女'), (1, '男'), (3, '保密')), default=3)
    address = models.CharField(verbose_name='地址', max_length=128, null=True, blank=True)

    class Meta:
        db_table = 'base_user'
        verbose_name = '基础用户'
        verbose_name_plural = verbose_name


class BaseModel(models.Model):
    create_time = models.TimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.TimeField(verbose_name='更新时间', auto_now_add=True)
    create_date = models.DateField(verbose_name='创建日期', auto_now_add=True)
    update_date = models.DateField(verbose_name='更新日期', auto_now_add=True)
    create_user = models.BigIntegerField(verbose_name='创建者', null=True,
                                         blank=True, help_text='创建者ID')

    class Meta:
        abstract = True


class UserImage(models.Model):
    image = models.ImageField(verbose_name='缩略图', upload_to='user', null=True, blank=True, max_length=128)
    user = models.OneToOneField(to='UserModel', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='头像')

    class Meta:
        db_table = 'user_image'
        verbose_name = '用户头像'
        verbose_name_plural = verbose_name


class SpiderModel(BaseModel):
    CHOICE = (
        ('hot_list', '综合热门'),
        ('All', '全部'),
        ('Bangumi', '番剧'),
        ('GuochuanAnime', '国产动画'),
        ('Guochuang', '国创相关'),
        ('Documentary', '纪录片'),
        ('Douga', '动画'),
        ('Music', '音乐'),
        ('Dance', '舞蹈'),
        ('Game', '游戏'),
        ('Knowledge', '知识'),
        ('Technology', '科技'),
        ('Sports', '运动'),
        ('Car', '汽车'),
        ('Life', '生活'),
        ('Food', '美食'),
        ('Animal', '动物圈'),
        ('Kitchen', '鬼畜'),
        ('Fashion', '时尚'),
        ('Ent', '娱乐'),
        ('Cinephile', '影视'),
        ('Movie', '电影'),
        ('TV', '电视剧'),
        ('Variety', '综艺'),
        ('Original', '原创'),
        ('Rookie', '新人'),
    )
    spider_name = models.CharField(max_length=128, verbose_name='爬虫名称')
    spider_states = models.BooleanField(verbose_name='爬虫状态', default=False)
    spider_field = models.CharField(max_length=128, verbose_name='关键字', choices=CHOICE)
    spider_page = models.IntegerField(verbose_name='爬取页数', blank=True, null=True)

    class Meta:
        db_table = 'spider'
        verbose_name = '爬虫表'
        verbose_name_plural = verbose_name


class Comment(BaseModel):
    r_pid = models.BigIntegerField(primary_key=True, verbose_name='评论ID')
    aid = models.ForeignKey(to='HotListModel', on_delete=models.SET_NULL, verbose_name='爬虫ID', null=True,
                            blank=True)
    mid = models.BigIntegerField(verbose_name='用户ID', blank=True, null=True)
    location = models.CharField(max_length=128, verbose_name='地区', default='无')
    content = models.CharField(max_length=512, verbose_name='评论内容', null=True, blank=True)
    referenceTime = models.DateTimeField(verbose_name='评论时间', null=True, blank=True)
    referenceName = models.CharField(max_length=128, verbose_name='评论名称', null=True, blank=True)
    referenceSex = models.CharField(max_length=128, verbose_name='评分', blank=True, null=True)

    class Meta:
        db_table = 'comment'
        verbose_name = '评论表'
        verbose_name_plural = verbose_name


class HotListModel(BaseModel):
    aid = models.BigIntegerField(primary_key=True, verbose_name='用户ID')
    view = models.BigIntegerField(verbose_name='播放量', null=True, blank=True)
    reply = models.BigIntegerField(verbose_name='评论量', null=True, blank=True)
    favorite = models.BigIntegerField(verbose_name='收藏量', null=True, blank=True)
    danmaku = models.BigIntegerField(verbose_name='弹幕量', null=True, blank=True)
    coin = models.BigIntegerField(verbose_name='投币量', null=True, blank=True)
    share = models.BigIntegerField(verbose_name='转发量', null=True, blank=True)
    his_rank = models.BigIntegerField(verbose_name='笔记量', null=True, blank=True)
    like = models.BigIntegerField(verbose_name='点赞量', null=True, blank=True)
    ctime = models.DateTimeField(verbose_name='创建时间', null=True, blank=True)
    pubdate = models.DateTimeField(verbose_name='更新时间', null=True, blank=True)
    pub_location = models.CharField(max_length=128, verbose_name='地址', null=True, blank=True)
    title = models.CharField(max_length=512, verbose_name='标题', null=True, blank=True)
    tname = models.CharField(max_length=512, verbose_name='分类', null=True, blank=True)
    owner_name = models.CharField(max_length=512, verbose_name='up主名称', null=True, blank=True)
    desc = models.CharField(max_length=1024, verbose_name='描述', null=True, blank=True)
    bvid = models.CharField(max_length=1024, verbose_name='BVID', null=True, blank=True)
    category = models.CharField(max_length=1024, verbose_name='分类', null=True, blank=True)
    spider = models.ForeignKey(to='SpiderModel', verbose_name='爬虫ID', on_delete=models.SET_NULL, null=True,
                               blank=True)

    class Meta:
        db_table = 'hot_list'
        verbose_name = '综合热门'
        verbose_name_plural = verbose_name
