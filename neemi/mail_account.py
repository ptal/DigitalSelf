import email
from imaplib import IMAP4

class MailAccount:
  def __init__(self, host, port, user, password, connection_security, authentication_method):
    self.host = host
    self.port = str(port)
    print(host)
    print(port)
    self.user = user
    self.password = password
    self.connection_security = connection_security
    self.authentication_method = authentication_method

  def imap4_connect(self):
    print ("connection...")
    connection = IMAP4(host=self.host, port=self.port)
    print ("launch starttls...")
    connection.starttls()
    print("login...")
    connection.login(self.user, self.password)
    print("list...")
    print (connection.list())
    print("logout...")
    connection.logout()
