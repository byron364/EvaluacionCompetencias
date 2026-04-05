from django import forms

class RegistroForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    rol = forms.ChoiceField(choices=[
        ('admin', 'Administrador'),
        ('soldado', 'Soldado'),
        ('instructor', 'Instructor'),
    ])