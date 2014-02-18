class BadAuthenticationMethod(Exception):
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return "Bad authentication method (" + self.value + ")"

class AuthenticationMethod:
  def __init__(self, user, password):
    self.user = user
    self.password = password

class NormalPasswordAuthentication(AuthenticationMethod):
  def authenticate(self, connection):
    connection.login(self.user, self.password)

def authentication_factory(auth_name, user, password):
  if (auth_name == 'normalpw'):
    return NormalPasswordAuthentication(user, password)
  else:
    raise BadAuthenticationMethod(auth_name)
