from django.conf import settings
from django.db import models


class Lockable(models.Model):
    lockable_seq = models.AutoField(primary_key=True)
    lockable_number = models.IntegerField(verbose_name='Lockable Number', default=0, null=False, blank=False)
    created_datetime = models.DateTimeField(verbose_name='Created Date', auto_now_add=True)
    updated_datetime = models.DateTimeField(verbose_name='Updated Date', auto_now=True)

    def __str__(self):
        return '%d(%d)' % (self.lockable_seq, self.lockable_number)

    class Meta:
        db_table = 'lockable'
        managed = getattr(settings, 'UNDER_TEST', True)
        verbose_name = 'Lockable'
        verbose_name_plural = verbose_name
