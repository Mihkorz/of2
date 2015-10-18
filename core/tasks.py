# -*- coding: utf-8 -*-

from __future__ import absolute_import

import time
import logging
from celery import shared_task

from core.models import Pathway

@shared_task(bind=True)
def countArr(self, path):
    pathway = Pathway.objects.get(id=path)
    arr=0
    for gene in pathway.gene_set.all():
        arr+=gene.arr
    
    return {pathway.name: arr}

@shared_task()
def add(x, y):
    
    
    time.sleep(5)
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)