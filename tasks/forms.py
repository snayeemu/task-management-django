from django import forms

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