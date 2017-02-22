#-*- coding: utf-8 -*-
from django.views.generic import TemplateView
from matching.models import Movies


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context