from imaplib import *

class BadConnectionSecurity(Exception):
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return "Bad connection security (" + self.value + ")"

class ConnectionSecurity:
  def __init__(self, host, port):
    self.host = host
    self.port = port

class SimpleSecurity(ConnectionSecurity):
  def make(self):
    return IMAP4(self.host, self.port)

class StarttlsSecurity(SimpleSecurity):
  def make(self):
    connection = super().make()
    connection.starttls()
    return connection

class SSLTLSSecurity(ConnectionSecurity):
  def make(self):
    return IMAP4_SSL(self.host, self.port)

def connection_factory(connection_name, host, port):
  if (connection_name == 'none'):
    return SimpleSecurity(host, port)
  elif (connection_name == 'starttls'):
    return StarttlsSecurity(host, port)
  elif (connection_name == 'ssltls'):
    return SSLTLSSecurity(host, port)
  else:
    raise BadConnectionSecurity(connection_name)
