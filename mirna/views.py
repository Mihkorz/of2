from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class TestView(TemplateView):
    template_name = 'project/project_detailll.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TestView, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(TestView, self).get_context_data(**kwargs)
        
        
        return context
