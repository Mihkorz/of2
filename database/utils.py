# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

def link_to_object(objectsList):
    """
    Used to draw related objects for models in Django Admin
    """
    total = objectsList.count()
    left = total - 5
    i = 0;
    html = ''
    for obj in objectsList:
        if i == 5:
            html+='<a href="Javascript:void(0)" style="color:#000;" onClick="django.jQuery(this).next().slideDown()">And '+str(left)+' more</a><div style="display:none">'
        i+=1
        url = reverse('admin:%s_%s_change' %(obj._meta.app_label,  obj._meta.module_name),  args=[obj.id] )
        html+= u'<a href="%s" style="display:block;">%s</a>' %(url,  obj.__unicode__())
    if total > 5:
        html+='<a href="Javascript:void(0)" style="color:#000;" onClick="django.jQuery(this).parent().slideUp()">Hide List</a>'
        html+='</div>'
    return html