import argparse
from mail_account import MailAccount
from mongoengine import connect

import sys

def main():
  parser = argparse.ArgumentParser(description='Retreive and store mails.')
  parser.add_argument('-s', required=True, help='Host of the email server.')
  parser.add_argument('-p', required=True, help='Port of the email server.')
  parser.add_argument('-u', required=True, help='User name of the email account.')
  parser.add_argument('-w', required=True, help='User password of the email account.')
  parser.add_argument('-c', required=True, help='Connection security method. Choose between \'none\', \'starttls\' or \'ssltls\'.')
  parser.add_argument('-a', required=True, help='Authentication method. Choose between \'normalpw\'.')
  parser.add_argument('-n', required=True, help='Neemi user pseudonym.')
  args = parser.parse_args()
  account = MailAccount(args.s, args.p, args.u, args.w, args.c, args.a)
  connect('digital_self')
  account.store(args.n)

if __name__ == "__main__":
  main()
