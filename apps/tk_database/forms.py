from django.forms import ModelForm
from apps.tk_database.models import Hike

class HikeForm(ModelForm):
    class Meta:
        model = Hike
        fields = [  'type',
                    'category',
                    'sub_category',
                    'region',
                    'title',
                    'description',
                    'image',
                    'leader',
                    'instructor',
                    'start_date',
                    'end_date',
                    'is_completed',
                    'is_private',
                    'is_full'
                ]