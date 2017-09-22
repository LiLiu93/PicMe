# User Module

# Extend the User class provided by Django
class UserProfile():
	gender_choices = (
		('M', 'Male'),
		('F', 'Female'),
		('U', 'Unknown')
	)

	user = models.OneToOneField(User, 
		on_delete=models.CASCADE,
		unique=True,
		verbose_name=_('user'),
		related_name='my_profile')

	nick_name  = models.CharField(max_length = 30)
	description = models.CharField(max_length=100,blank = True,null=True)
	gender = models.CharField(max_length=1, choices=gender_choices, default='U') 
	level = models.IntegerField(default=1)

# Address Model
# We assume that all the states and cities can be stored in the database in a same table.
class District(models.Model):
	code = models.IntegerField(primary_key=True)
	name = models.CharField(max_length = 50)

class UserAddress(models.Model):
	user = models.ForeignKey(UserProfile, 
		on_delete=models.CASCADE)

	user_state = models.ForeignKey(District, 
		related_name='user_state')
	user_city = models.ForeignKey(District, 
		related_name='user_city')
	postcode = models.PositiveIntegerField(blank = False)

# Post Module
class Post(TimeStampedModel):
	# basic
	post_title = models.CharField(max_length=200,
		null =False)
	post_description = models.TextField()
	
	# picture
	post_picture = models.ImageField(null=False,
		blank = False
	)

	# The location of the picture
	post_state = models.ForeignKey(District, 
		related_name='state')
	post_city = models.ForeignKey(District,
		related_name='city')

	# user who creates the post 
	user = models.ForeignKey(UserProfile)

# Chat Module
class Chat(TimeStampedModel):
	sender = models.ForeignKey(User, default=None)
	receiver = models.ForeignKey(User, default=None)
	content = models.CharField(max_length=160)