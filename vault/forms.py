from django import forms
from .models import Contact, Link, Password

# ---------------- Contact Form -----------------
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'phone', 'email', 'notes', 'group']

# ---------------- Link Form -----------------
class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['title', 'url', 'category', 'notes']

# ---------------- Password Form -----------------
class PasswordForm(forms.ModelForm):
    # আমরা plain password field বানাচ্ছি যা user input নিবে
    password_plain = forms.CharField(
        widget=forms.PasswordInput(),
        label="Password"
    )

    class Meta:
        model = Password
        # password_encrypted remove করেছি
        fields = ['service_name', 'username', 'notes']
