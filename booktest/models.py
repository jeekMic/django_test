from django.db import models


class BookInfo(models.Model):
    btitle = models.CharField(max_length=20)
    bpub_date = models.DateTimeField()
    bread = models.IntegerField(default=0)
    bcommet = models.IntegerField(default=0)
    isDelete = models.BooleanField(default=False)
    # db_table表示设置数据库中表的名字，如果不设置，则前面会带上booktest这个前缀
    class Meta:
        db_table = 'bookinfo'
    # 默认的是objects books = models.Manager()
    @classmethod
    def create(cls,btitle, bpub_date):
        b = BookInfo()
        b.btitle = btitle
        b.bpub_date = bpub_date
        b.bread = 0
        b.bcommet = 0
        b.isDelete = False
        return b



class HeroInfo(models.Model):
    hname = models.CharField(max_length=20)
    hgender = models.BooleanField(default=True)
    isDelete = models.BooleanField(default=False)
    hcontent = models.CharField(max_length=100)
    # django新特性，需要在后面添加on_delete=models.CASCADE
    hbook = models.ForeignKey('BookInfo', on_delete=models.CASCADE,)
    # 这个方法供html里面的调用，调用一般是 obj.arrt 第一步是以字典的形式来查找，第二步是以类属性来查找，第三次是以类方法来调用，最后是以索引值来查找
    def showname(self):
        return self.hname
