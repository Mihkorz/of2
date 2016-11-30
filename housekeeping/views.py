import json

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from django.views.generic.base import TemplateView, View

from essence.pathways import maxim_format_pathway
from housekeeping.forms import UpdatePathwayForm
from oncofinder_utils.django_helpers import MessageLog


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

            maxim_format_pathway(task_args['filepath'], task_args['organism'], task_args['database'], None)

            return HttpResponse(json.dumps({}), mimetype='application/json; charset=utf-8')
        else:
            raise ValueError('Unknown task "{}".'.format(task))


class HousekeepingPathwayView(FormView):

    form_class = UpdatePathwayForm
    success_url = reverse_lazy('HousekeepingPathwayView')
    template_name = 'housekeeping/pathway.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(HousekeepingPathwayView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        dct = form.cleaned_data
        message_log = MessageLog(self.request)
        maxim_format_pathway(dct['filename'], dct['organism'], dct['database'], message_log)
        return super(HousekeepingPathwayView, self).form_valid(form)
