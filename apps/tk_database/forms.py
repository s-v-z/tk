from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form, CharField
from django.forms.widgets import DateInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from apps.tk_database.models import Hike

class HikeForm(ModelForm):
    class Meta:
        model = Hike
        fields = [  'type', 'category', 'sub_category', 'region', 'title', 'description', 'image',
        'leader', 'instructor', 'start_date', 'end_date', 'is_completed', 'is_private', 'is_full' ]
        widgets = {
            # TODO: разобраться с форматом даты в инпуте. сейчас он почему-то игнорируется.
            'start_date': DateInput(format='%Y-%m-%d', attrs={'class':'form-control', 'placeholder':'Выберите дату', 'type':'date'}),
            'end_date': DateInput(format='%Y-%m-%d', attrs={'class':'form-control', 'placeholder':'Выберите дату', 'type':'date'}),
        }

    def __init__(self, *args, **kwargs):
        action = kwargs.pop('action', None)
        submit_label = kwargs.pop('submit_label', 'Сохранить')

        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.fields['type'].label = 'Вид похода'
        self.fields['category'].label = 'Категория'
        self.fields['sub_category'].label = 'С элементами'
        self.fields['region'].label = 'Район похода'
        self.fields['title'].label = 'Название мероприятия/походной группы'
        self.fields['description'].label = 'Описание'
        self.fields['image'].label = 'Картинка для привлечения внимания'
        self.fields['leader'].label = 'Руководитель'
        self.fields['instructor'].label = 'Инструктор'
        self.fields['start_date'].label = 'Дата начала'
        self.fields['end_date'].label = 'Дата окончания'
        self.fields['is_completed'].label = 'Поход завершён'
        self.fields['is_private'].label = 'Не отображать в списке походов'
        self.fields['is_full'].label = 'Группа набрана'

        for field in self.fields.values():
            if field.required:
                field.error_messages = {'required': 'Это поле обязательное'}

        self.helper.form_id = f"id-hike-{action}-form"
        self.helper.form_class = f"hike-{action}-class"
        self.helper.attrs = {"novalidate": ''}

        self.helper.add_input(Submit('submit', submit_label))

class DeleteConfirmationForm(Form):
    confirmation = CharField(label='Я хочу', max_length=20, required=False)

    def clean_confirmation(self):
        data = self.cleaned_data['confirmation']
        if data.casefold() != 'удалить поход':
            raise ValidationError("Для удаления похода напишите в этом поле 'удалить поход'")
