from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

User = get_user_model()

class UserForm(UserChangeForm):
   class Meta:
      model = User
      fields = "__all__"


class UserCustomCreationForm(UserCreationForm):
   class Meta:
      model = User
      fields = "__all__"
