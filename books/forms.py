from django import forms
from .models import Book
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_date']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
        }

class BookSearchForm(forms.Form):
    q = forms.CharField(label='검색', required=False)

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class BookLoanForm(forms.Form):
    book = forms.ModelChoiceField(queryset=Book.objects.all(), label='대여할 도서')
    loan_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='대여 시작일')
    return_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='반납 예정일')
    reason = forms.CharField(widget=forms.Textarea, label='대여 사유')

    def clean(self):
        cleaned_data = super().clean()
        loan_date = cleaned_data.get('loan_date')
        return_date = cleaned_data.get('return_date')

        if loan_date and return_date and loan_date > return_date:
            raise forms.ValidationError("반납 예정일은 대여 시작일보다 늦어야 합니다.")

        return cleaned_data
