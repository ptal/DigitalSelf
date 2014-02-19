from mongoengine.connection import get_db

class MailAnalyser:
  def __init__(self, username):
    self.username = username

  def analyse(self, mail):
    pass