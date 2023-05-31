class AbstractUser:
	role = lambda self: self.__str__()
	is_superuser = lambda self: False
	is_manager = lambda self: False
	is_staff = lambda self: False
	is_anon = lambda self: False

	def __str__(self)  -> str:
		return str(__name__).lower()

class Manager(AbstractUser):
	is_manager = lambda self: True
	is_staff = lambda self: True

class Teacher(AbstractUser):
	is_staff = lambda self: True

	
class Anonymous(AbstractUser):
	is_anon = lambda self: True

class Admin(AbstractUser):
	is_superuser = lambda self: True
	is_manager = lambda self: True
	is_staff = lambda self: True