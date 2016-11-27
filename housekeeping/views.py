# -*- coding: utf-8 -*-

import os
import csv
import numpy as np
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from pandas import read_csv, read_excel, DataFrame, Series
from scipy.stats.mstats import gmean
from scipy.stats import ttest_1samp, norm as scipynorm
from sklearn.metrics import roc_auc_score

import itertools
import json
import logging

from django.views.generic.base import TemplateView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.conf import settings

from core.models import Pathway, Gene, Node, Component, Relation
from database.models import Pathway as oPath, Gene as oGene, Node as oNode, Component as oComp, Relation as oREl
from essence.pathways import maxim_format_pathway
from metabolism.models import MetabolismPathway
from mouse.models import MouseMetabolismPathway, MousePathway, MouseMapping
# from .stats import fdr_corr
from housekeeping.forms import UpdatePathwayForm


class HousekeepingView(TemplateView):

    template_name = 'housekeeping/index.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(HousekeepingView, self).dispatch(request, *args, **kwargs)


class HousekeepingAjaxView(View):

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        dct = json.loads(request.body)

        task = dct.get('task')
        if task is None:
            raise ValueError('Missing "task" param.')

        if task == 'update_pathway':
            task_args = dct.get('args')
            if task_args is None:
                raise ValueError('Missing "task_args" param.')

            maxim_format_pathway(task_args['filepath'], task_args['organism'], task_args['database'])

            return HttpResponse(json.dumps({}), mimetype='application/json; charset=utf-8')
        else:
            raise ValueError('Unknown task "{}".'.format(task))


class HousekeepingPathwayView(FormView):

    template_name = 'housekeeping/pathway.html'
    form_class = UpdatePathwayForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(HousekeepingPathwayView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # return HttpResponseRedirect(reverse('document_detail', args=(output_doc.id,)))
        return HttpResponseRedirect('pathway')


