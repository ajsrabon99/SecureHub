from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Contact, Link, Password
from .forms import ContactForm, LinkForm, PasswordForm
from cryptography.fernet import Fernet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Encryption key (save in safe place)
key = b'pD7bddJPzx-s3RE-S3ufOmTxjvouQQiIhadoZxoFHEQ='
f = Fernet(key)


@login_required
def home(request):
    recent_contacts = Contact.objects.filter(user=request.user).order_by('-id')[:5]
    recent_links = Link.objects.filter(user=request.user).order_by('-id')[:5]
    recent_passwords = Password.objects.filter(user=request.user).order_by('-id')[:5]
    # Decrypt passwords
    for p in recent_passwords:
        try:
            p.password_decrypted = f.decrypt(p.password_encrypted).decode()
        except:
            p.password_decrypted = 'Error'
    context = {
        'contacts': recent_contacts,
        'links': recent_links,
        'passwords': recent_passwords
    }
    return render(request, 'vault/home.html', context)


# ---------------- Contact Views -----------------
@login_required
def contact_list(request):
    contacts = Contact.objects.filter(user=request.user)
    return render(request, 'vault/contact_list.html', {'contacts': contacts})

@login_required
def contact_add(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('contact_list')
    else:
        form = ContactForm()
    return render(request, 'vault/contact_form.html', {'form': form})

@login_required
def contact_edit(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contact_list')
    else:
        form = ContactForm(instance=contact)
    return render(request, 'vault/contact_form.html', {'form': form})

@login_required
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    contact.delete()
    return redirect('contact_list')

# ---------------- Link Views -----------------
@login_required
def link_list(request):
    links = Link.objects.filter(user=request.user)
    return render(request, 'vault/link_list.html', {'links': links})

@login_required
def link_add(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.user = request.user
            link.save()
            return redirect('link_list')
    else:
        form = LinkForm()
    return render(request, 'vault/link_form.html', {'form': form})

@login_required
def link_edit(request, pk):
    link = get_object_or_404(Link, pk=pk, user=request.user)
    if request.method == 'POST':
        form = LinkForm(request.POST, instance=link)
        if form.is_valid():
            form.save()
            return redirect('link_list')
    else:
        form = LinkForm(instance=link)
    return render(request, 'vault/link_form.html', {'form': form})

@login_required
def link_delete(request, pk):
    link = get_object_or_404(Link, pk=pk, user=request.user)
    link.delete()
    return redirect('link_list')

# ---------------- Password Views -----------------
@login_required
def password_list(request):
    passwords = Password.objects.filter(user=request.user)
    # Decrypt password for display
    for p in passwords:
        try:
            p.password_decrypted = f.decrypt(p.password_encrypted).decode()
        except:
            p.password_decrypted = 'Error'
    return render(request, 'vault/password_list.html', {'passwords': passwords})

@login_required
def password_add(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            pwd = form.save(commit=False)
            pwd.user = request.user
            # Encrypt the plain password from form
            pwd.password_encrypted = f.encrypt(form.cleaned_data['password_plain'].encode())
            pwd.save()
            return redirect('password_list')
    else:
        form = PasswordForm()
    return render(request, 'vault/password_form.html', {'form': form})

@login_required
def password_edit(request, pk):
    pwd = get_object_or_404(Password, pk=pk, user=request.user)
    if request.method == 'POST':
        form = PasswordForm(request.POST, instance=pwd)
        if form.is_valid():
            pwd = form.save(commit=False)
            pwd.user = request.user
            pwd.password_encrypted = f.encrypt(form.cleaned_data['password_plain'].encode())
            pwd.save()
            return redirect('password_list')
    else:
        # Set initial value for password_plain as decrypted password
        try:
            initial_password = f.decrypt(pwd.password_encrypted).decode()
        except:
            initial_password = ''
        form = PasswordForm(instance=pwd, initial={'password_plain': initial_password})
    return render(request, 'vault/password_form.html', {'form': form})

@login_required
def password_delete(request, pk):
    pwd = get_object_or_404(Password, pk=pk, user=request.user)
    pwd.delete()
    return redirect('password_list')


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Signup এর সাথে সাথে login
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'vault/signup.html', {'form': form})