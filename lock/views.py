import logging
import time

from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView

from lock.models import Lockable

logger = logging.getLogger('default')


class TestLockViewSet(APIView):

    def get(self, request):
        _data = int(request.GET.get('data'))
        _return_data = {
            'code': 0,
            'message': 'OK',
        }
        try:
            _lockable = self._transaction_get(_data)
            _return_data['result'] = str(_lockable)
        except Exception as e:
            logger.error('exception: ' + str(e))
            _return_data['result'] = str(e)
        return Response(status=200, data=_return_data)

    WAIT = 10

    @transaction.atomic
    def _transaction_get(self, data):
        _lockable = Lockable.objects.select_for_update().get(pk=1)

        logger.debug('select lockable row %s...' % str(_lockable))
        for i in range(self.WAIT):
            logger.debug('waiting %s seconds...' % (self.WAIT - i))
            time.sleep(1)
        _lockable.lockable_number += data
        logger.debug('updating lockable row %s...' % str(_lockable))
        _lockable.save()
        logger.debug('updated lockable row %s...' % str(_lockable))

        try:
            _lockable = self._transaction_get2(data, raise_exception=True)
        except Exception as e:
            logger.error(str(e))

        _lockable = self._transaction_get2(data)

        logger.debug('select lockable row %s...' % str(_lockable))
        for i in range(self.WAIT):
            logger.debug('waiting %s seconds...' % (self.WAIT - i))
            time.sleep(1)
        _lockable.lockable_number += data
        logger.debug('updating lockable row %s...' % str(_lockable))
        _lockable.save()
        logger.debug('updated lockable row %s...' % str(_lockable))

        return self._transaction_get2(data)

    @transaction.atomic
    def _transaction_get2(self, data, raise_exception=False):
        _lockable = Lockable.objects.select_for_update().get(pk=1)
        logger.debug('select lockable row %s...' % str(_lockable))
        for i in range(self.WAIT):
            logger.debug('waiting %s seconds...' % (self.WAIT - i))
            time.sleep(1)
        _lockable.lockable_number += data
        logger.debug('updating lockable row %s...' % str(_lockable))
        _lockable.save()
        logger.debug('updated lockable row %s...' % str(_lockable))
        if raise_exception:
            logger.debug('Raise exception with lockable row %s...' % str(_lockable))
            raise Exception('Test exception...')
        return _lockable
