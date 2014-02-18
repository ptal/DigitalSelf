import email
from imaplib import *
from connection_security import connection_factory
from authentication_method import authentication_factory

from mongoengine.connection import get_db

class MailAccount:
  def __init__(self, host, port, user, password, connection_security, authentication_method):
    connection_maker = connection_factory(connection_security, host, str(port))
    authentication = authentication_factory(authentication_method, user, password)
    self.mail_server = connection_maker.make()
    authentication.authenticate(self.mail_server)

  def store(self):
    print (self.mail_server.list())

  def __logout(self):
    self.mail_server.logout()
