from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from neemi.data import get_user_data, get_all_user_data
from neemi.search import simple_keyword_search
from neemi.stats import *
from neemi.mail_account import *
from forms import *
import time, datetime

def index(request, template='index.html'):
    login_form = LoginForm()
    context = RequestContext(request, {'login_form':login_form})
    response = render_to_response(template, locals(), context_instance=context)
    return response

def register(request, template='register.html'):
    if request.method == 'POST':
        mail_form = MailAccountForm(request.POST)
        if mail_form.is_valid():
            mail_account = MailAccount(
                mail_form.cleaned_data['server_addr'],
                mail_form.cleaned_data['server_port'],
                mail_form.cleaned_data['user_name'],
                mail_form.cleaned_data['user_password'],
                mail_form.cleaned_data['connection_security'],
                mail_form.cleaned_data['authentication_method'])
            mail_account.imap4_connect()
    else:
        mail_form = MailAccountForm()
    context = RequestContext(request, {'mail_account_form':mail_form, 'services':SERVICE_CHOICES})
    response = render_to_response(template, locals(), context_instance=context)
    return response

def search(request, template='search.html'):
    if request.method == 'POST':
        form = KeywordSearchForm(request.POST)
        if form.is_valid():
            print [form.data]
            print "GOOD DATA"
            print [form.cleaned_data]
            return simple_keyword_search(request=request,
                                         keyword=form.cleaned_data['keyword'],
                                         service=form.cleaned_data['service'])
        else:
            print "invalid form"
            dform = form
    else:
        dform = KeywordSearchForm()
    context = RequestContext(request,{'form':dform})
    response = render_to_response(template, locals(), context_instance=context)
    return response

def query_results(request, template='results.html'):
    context = RequestContext(request)
    response = render_to_response(template, locals(), context_instance=context)
    return response

def get_data(request, template='data.html'):
    if request.method == 'POST':
        form = GetDataForm(request.POST)
        if form.is_valid():
            print [form.data]
            print "GOOD DATA"
            print [form.cleaned_data]
            if 'bt_search' in form.data:
                return get_all_user_data(request=request,
                                         service=form.cleaned_data['service'])
            elif 'bt_get_data_since' in form.data:
                return get_user_data(request=request,
                                     service=form.cleaned_data['service'],
                                     from_date="since_last",
                                     to_date=None,
                                     lastN=None)
            else:
                if form.cleaned_data['from_date'] != None:
                    from_date_epoch=int(time.mktime(form.cleaned_data['from_date'].timetuple()))//1*1000
                else:
                    from_date_epoch = None

                if form.cleaned_data['to_date'] != None:
                    to_date_epoch=int(time.mktime(form.cleaned_data['to_date'].timetuple()))//1*1000
                else:
                    to_date_epoch=None
        
                return get_user_data(request=request,
                                     service=form.cleaned_data['service'],
                                     from_date=from_date_epoch,
                                     to_date=to_date_epoch,
                                     lastN=form.cleaned_data['lastN'])
        else:
            print "invalid form"
            dform = form
    else:
        dform = GetDataForm()
    context = RequestContext(request,{'form':dform})
    response = render_to_response(template, locals(), context_instance=context)
    return response


def delete(request, template='delete.html'):
    context = RequestContext(request)
    response = render_to_response(template, locals(), context_instance=RequestContext(request))
    return response

def get_stats(request, template='stats.html'):
    if request.method == 'GET':
        stats = DBAnalysis(request)
        html_stats = stats.basic_stats()   

    response = render_to_response(template, locals(), context_instance=RequestContext(request))
    return response

def error(request, template='error.html'):
    message = request.GET.get('message')
    print "Message: ", message
    response = render_to_response(template, locals(), context_instance=RequestContext(request))
    return response


