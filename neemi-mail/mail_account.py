import email
from imaplib import *
import re, io
from connection_security import connection_factory
from authentication_method import authentication_factory

from mail_analyser import *

mailboxlist_regex = re.compile('\\(([^[)]*)\\) "([^"]*)" "([^"]*)"')

def utf8_join(iterable, sep):
  res = str()
  for e in iterable:
    res += str(e, encoding='utf8') + sep
  return res

class MailAccount:
  def __init__(self, host, port, user, password, connection_security, authentication_method):
    connection_maker = connection_factory(connection_security, host, str(port))
    authentication = authentication_factory(authentication_method, user, password)
    self.mail_server = connection_maker.make()
    authentication.authenticate(self.mail_server)

  def store(self, username):
    analyser = MailAnalyser(username)
    result, mailboxes = self.mail_server.list()
    if(result == 'OK'):
      for mailbox in mailboxes:
        flags, delimiter, mailbox_name = mailboxlist_regex.match(str(mailbox, encoding='utf8')).groups()
        # We want the mailbox to be selectable.
        if not "\\noSelect" in flags:
          print (mailbox_name)
          result, data = self.mail_server.select(mailbox_name, readonly=True)
          print(data)
          if(result == 'OK'):
            result, data = self.mail_server.search(None, 'ALL')
            if(result == 'OK'):
              mail_ids = str(b' '.join(data), encoding='utf8').split()
              for mail_id in mail_ids:
                result, msg_data = self.mail_server.fetch(mail_id, "RFC822")
                if(result == 'OK'):
                  for response_part in msg_data:
                    if isinstance(response_part, tuple):
                      analyser.analyse(response_part[1])
                else:
                  print("fetch: " + result + " " + data)
            else:
              print("search: " + result + " " + data)
          else:
            print("select: " + result)
      analyser.save()
    else:
      print('Cannot list mailboxes.')

  def logout(self):
    self.mail_server.logout()

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    self.logout()
