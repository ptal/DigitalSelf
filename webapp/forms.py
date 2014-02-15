import datetime
from django import forms
from django.contrib.admin import widgets
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import Select

SERVICE_CHOICES=[('facebook','Facebook'),
                 ('foursquare','foursquare'),
                 ('twitter','Twitter'),
                 ('linkedin','LinkedIn'),
                 ('gmail','Gmail'), 
                 ('gcal','Google Calendar'),
                 ('googleplus', 'Google+'),
                 #('googledrive','Google Drive'),#Need to download files separately
                 ('googlecontacts', 'Google Contacts'),
                 ('dropbox','Dropbox'),
                 #('amex','Amex')
                 #      'Instagram',
                # 'Tumblr',
                #'FitBit',
                #GoogleDocs',
                #GooglePicasa'
                ]

  
    #YEAR_CHOICES = reversed(range(2005,2013))


class GetDataForm(forms.Form):
    service = forms.ChoiceField(label="Service",choices=SERVICE_CHOICES)
    #from_date = forms.DateField(label="From (optional)",widget=SelectDateWidget(years=range(2013,2005,-1)),required=False)
    #to_date = forms.DateField(label="To (optional)",widget=SelectDateWidget(years=range(2013,2005,-1)),required=False)
    #lastN = forms.IntegerField(label="Result limit (optional)", required=False)

class KeywordSearchForm(forms.Form):
    service = forms.ChoiceField(label="Service",choices=SERVICE_CHOICES)
    keyword = forms.CharField(label="Search",required=True)

class MailAccountForm(forms.Form):
    server_name = forms.URLField(label="Server address")
    server_port = forms.DecimalField(label="Server port", min_value=0, max_value= 65535)
    user_name = forms.CharField(label="User name")
    user_password = forms.CharField(label="User password", widget=forms.PasswordInput)
    connection_security = forms.ChoiceField(label="Connection security", choices=[('none','None'),('starttls','STARTTLS'),('ssltls','SSL/TLS')])
    authentication_method = forms.ChoiceField(label="Authentication Method", choices=[('noramlpw','Normal password')])

class LoginForm(forms.Form):
    login = forms.CharField(label="Login")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
