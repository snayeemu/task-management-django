from django import forms
from django.forms import ModelForm
from tasks.models import Tasks

# django form
class TaskForm(forms.Form):
    CHOICES = [5, 8]
    title = forms.CharField(label = "Task Title", max_length=100)
    description = forms.CharField(label = "Task Description", widget=forms.Textarea)
    due_date = forms.DateField(label="Due Date", widget=forms.SelectDateWidget)
    assigned_to = forms.MultipleChoiceField(label="Employees/Assigned_To", choices=[], widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        # print(args, kwargs)
        employees = kwargs.pop("employees", [])
        super().__init__(*args, **kwargs)
        self.fields["assigned_to"].choices = [(employee.id, employee.name) for employee in employees]

class StyledFormMixin:
    """ Mixing to apply style to form field """

    default_classes = "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    "class": self.default_classes,
                    "placeholder": f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    "class": self.default_classes,
                    "placeholder": f"Enter {field.label.lower()}",
                    "rows": 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    "class": "shadow appearance-none border rounded w-xl py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                })
            elif isinstance(field.widget, forms.SelectMultiple):
                field.widget.attrs.update({
                    "class": "space-y-2"
                })
        


# django model form
class TaskModelForm(StyledFormMixin, ModelForm):
    class Meta:
        model = Tasks
        # fields = "__all__"
        # exclude = ["project", "is_completed", "created_at", "updated_at"]
        fields = ["title", "description", "due_date", "employees"]

        widgets = {
            "due_date": forms.SelectDateWidget,
            "employees": forms.CheckboxSelectMultiple
        }

        """ Manual Widget """
        # widgets = {
        #     "title": forms.TextInput(attrs={
        #         "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline" ,
        #         "placeholder": "Enter Task Title"
        #     }),
        #     "due_date": forms.SelectDateWidget(attrs={
        #         "class": "shadow appearance-none border rounded w-xl py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        #     }),
        #     "description": forms.Textarea(attrs={
        #         "class": "shadow appearance-none border rounded w-full h-[20px] py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
        #         "placeholder": "Enter Task Description",
        #         "rows": 3
        #         }),
        #     "employees": forms.CheckboxSelectMultiple()
        # }

    """ Widget Using Mixin """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()