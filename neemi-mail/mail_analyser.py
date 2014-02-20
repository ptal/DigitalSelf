import pymongo
from pymongo import MongoClient

import email
from email.header import decode_header
from email.parser import BytesParser

class Person:
  def __init__(self, name, email):
    self.emails = set()
    self.addEmail(email)
    self.name = name
    self.relations = {}

  def knows(self, p):
    for m in p.emails:
      self.relations[m] = p
      break

  def addEmail(self, email):
    self.emails.add(email.lower())

  def to_schema(self):
    # Boolean attribute without value are forbidden in XML, so we use the "empty string" syntax.
    root = etree.Element("div", itemscope="", itemtype="http://schema.org/Person")
    etree.SubElement(root, "span", itemprop="name").text = self.name

    for mail in self.emails:
      etree.SubElement(root, "span", itemprop="email").text = mail

    for relation in self.relations.values():
      relation_filename = make_person_filename(relation)
      etree.SubElement(root, "a", href=relation_filename, itemprop="knows").text = relation.name
    return root

  def to_string_schema(self):
    return str(etree.tostring(self.to_schema(), method="html", encoding="utf-8", pretty_print=True), encoding="utf-8")

  def merge(self, p):
    self.emails = self.emails.union(p.emails)
    # TODO try to find the better name.
    self.relations.update(p.relations)
    return self


def relateTwoPersons(p1, p2):
  if p1 and p2:
    p1.knows(p2)
    p2.knows(p1)

def merge_person(p1, p2):
  if p1 == None:
    return p2
  elif p2 == None:
    return p1
  else:
    return p1.merge(p2)

def make_utf8_str(s):
  res = ""
  for (data, encoding) in decode_header(s):
    if data != None and encoding != None:
      res += str(data.decode(encoding).encode("utf-8"), "utf-8")
    else:
      res += str(data)
  return res

class MailAnalyser:
  def __init__(self, username):
    self.username = username
    self.person_db = {}

  # TODO
  def save():
    client = MongoClient()
    db = client['digital_self']
    all_collections = db.collection_names()
    if self.username in all_collections:
      pass

  def guess_name_from_mail_addr(self, mailAddr):
    return mailAddr.partition('@')[0]

  def find_person(self, p):
    for email in p.emails:
      if email in self.person_db:
        return self.person_db[email]
    return None

  def update_db(self, person):
    for email in person.emails:
      if email in self.person_db:
        person = merge_person(person, self.person_db[email])
    for email in person.emails:
      self.person_db[email] = person

  def mail_info(self, realname, mailAddr):
    realname = make_utf8_str(realname)
    mailAddr = make_utf8_str(mailAddr.lower())
    if not realname:
      realname = self.guess_name_from_mail_addr(mailAddr)
    return (realname, mailAddr)

  def link_people(self, myself, contacts_field):
    contacts_field = email.utils.getaddresses(contacts_field)
    if contacts_field:
      people = set()
      for (name, email_addr) in contacts_field:
        (name, email_addr) = self.mail_info(name, email_addr)
        if email_addr not in self.person_db or self.person_db[email_addr] != myself:
          self.update_db(Person(name, email_addr))
          people.add(email_addr)
      for mail in people:
        relateTwoPersons(self.person_db[mail], myself)

    # Find cc and to relation (excluding ourself)
    self.link_people(me, msg.get_all('to', []))
    self.link_people(me, msg.get_all('cc', []))

  def get_info_from_mail_field(self, field):
    (realname, mailAddr) = email.utils.parseaddr(field)
    return self.mail_info(realname, mailAddr)

  def analyse(self, mail):
    msg = BytesParser().parsebytes(mail)
    # Retrieve the from person.
    (realname, mailAddr) = self.get_info_from_mail_field(msg['from'])
    person = Person(realname, mailAddr)

    # Add it to the database.
    self.update_db(person)

    # Find ourself
    (my_name, my_email) = self.get_info_from_mail_field(msg['Delivered-To'])
    me = Person(my_name, my_email)

    def addToMyEmailAddr(field_name):
      (_, my_email_addr) = self.get_info_from_mail_field(msg[field_name])
      if my_email_addr:
        me.addEmail(my_email_addr)

    addToMyEmailAddr('Resent-From')

    self.update_db(me)
