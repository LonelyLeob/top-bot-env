class AbstractUser:
	def __str__(self)->str:
		return str(__name__).lower()

	def role(self)->str:
		""""alias for __str__ method"""
		return self.__str__()

	def is_superuser(self) -> bool:
		return False

class Manager(AbstractUser):
	pass

class Teacher(AbstractUser):
	pass

class Anonymous(AbstractUser):
	pass

class Admin(AbstractUser):
	def is_superuser(self) -> bool:
		return True