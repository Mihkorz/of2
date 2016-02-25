# -*- coding: utf-8 -*-
import json
from pandas import  DataFrame, Series, read_csv

from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings

class DemoReport(TemplateView):
    template_name = "website/demo-report.html"
    
    
    def dispatch(self, request, *args, **kwargs):
        
        return super(DemoReport, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
              
        context = super(DemoReport, self).get_context_data(**kwargs)
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        
        import datetime
        now = datetime.datetime.now().strftime('%D %H:%M:%S')
        
        try:
            counter_df = read_csv(settings.MEDIA_ROOT+'/report-counter.csv', index_col=0)
        except:
            counter_df = DataFrame(columns=['ip', 'datetime'])
        
        new_visitor = DataFrame.from_dict({'ip': [ip], 'datetime':[now]}, orient='columns')
        
        counter_df1 = counter_df.append(new_visitor)
        counter_df1.to_csv(settings.MEDIA_ROOT+'/report-counter.csv')
        
        context['test'] = "TEst"
        
        return context
    
class ReportJson(TemplateView):
    template_name="website/report.html"
    def dispatch(self, request, *args, **kwargs):
        
        return super(ReportJson, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        
        gene_name = request.GET.get('gene')
        
        df = read_csv(settings.MEDIA_ROOT+"/../static/report/demo/counts_norm_all.txt",
                      sep='\t')
        
        df.set_index('SYMBOL', inplace=True)
        #raise Exception('stop')
        gene_row = df.loc[gene_name]
        
        STP1657 = round(gene_row['SPT1657_SPT1663'],2)
        STP1658 = round(gene_row['SPT1658_SPT1664'],2)
        STP1659 = round(gene_row['SPT1659_SPT1665'],2)
        STP1660 = round(gene_row['SPT1660_SPT1666'],2)
        STP1661 = round(gene_row['SPT1661_SPT1667'],2)
        STP1662 = round(gene_row['SPT1662_SPT1668'],2)
        
        response_data = {}
        
        response_data['Unsorted'] = [
                   ['SPT1657/SPT1663', STP1657],
                   ['SPT1658/SPT1664', STP1658],
                   ['SPT1659/SPT1665', 0],
                   ['SPT1660/SPT1666', 0],
                   ['SPT1661/SPT1667', 0],
                   ['SPT1662/SPT1668', 0]
                   ]
        response_data['Low'] = [
                   ['SPT1657/SPT1663', 0],
                   ['SPT1658/SPT1664', 0],
                   ['SPT1659/SPT1665', STP1659],
                   ['SPT1660/SPT1666', STP1660],
                   ['SPT1661/SPT1667', 0],
                   ['STP1662', 0]
                   ]
        response_data['High'] = [
                   ['SPT1657/SPT1663', 0],
                   ['SPT1658/SPT1664', 0],
                   ['SPT1659/SPT1665', 0],
                   ['SPT1660/SPT1666', 0],
                   ['SPT1661/SPT1667', STP1661],
                   ['SPT1662/SPT1668', STP1662]
                   ]
        
        
        
        return HttpResponse(json.dumps(response_data), content_type="application/json")