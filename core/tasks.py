# -*- coding: utf-8 -*-

from __future__ import absolute_import


import logging
from celery import shared_task


@shared_task(bind=True)
def add(self, x, y):
    self.update_state(state='PROGRESS')
    import time
    time.sleep(5)
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)