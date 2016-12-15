import json
import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from django.views.generic.base import TemplateView, View

from core.models import import_pathway
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

            import_pathway(task_args['filepath'], task_args['organism'], task_args['database'])

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
        file_obj = self.request.FILES['filename']
        try:
            import_pathway(file_obj, dct['organism'], dct['database'])
            messages.success(self.request, 'Successfully completed.')
        except Exception as ex:
            messages.error(self.request, 'Error: {}'.format(ex))

        return super(HousekeepingPathwayView, self).form_valid(form)


class ChangelogView(TemplateView):

    template_name = 'housekeeping/changelog.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ChangelogView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ChangelogView, self).get_context_data(**kwargs)

        fname = os.path.join(settings.PROJECT_DIR, '..', 'changelog.txt')
        with open(fname) as f:
            context['changelog'] = f.read()

        return context
