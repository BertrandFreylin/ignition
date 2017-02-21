#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    text = """<h1>Ignition program</h1>"""
    return HttpResponse(text)