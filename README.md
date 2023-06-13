## DJ Notes

### A Note taking app powered by Django

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

[![Deploy on Railway](https://railway.app/button.svg)](https://dj-notes.up-railway.app)

### What is DJ Notes

- A Note Taking App
- Collect your thoughts in the form of notes or collections of notes(books)
- Secure Note taking experience
- Markdown Support

### Tech Stack

- Django
- PostgreSQL
- Nixpack
- Cookiecutter Template

### Preview

<img src="https://res.cloudinary.com/techstructive-blog/image/upload/v1656861308/blog-media/djnotes-home.png" height="300px" width="450px"> <img src="https://res.cloudinary.com/techstructive-blog/image/upload/v1656861556/blog-media/dj-notes-note-preview.png" height="300px" width="450px">

## DJ Notes's ER Diagram

```mermaid
erDiagram
Permission{
AutoField id
CharField name
CharField codename
}
Group{
AutoField id
CharField name
}
ContentType{
AutoField id
CharField app_label
CharField model
}
Session{
CharField session_key
TextField session_data
DateTimeField expire_date
}
Site{
AutoField id
CharField domain
CharField name
}
LogEntry{
AutoField id
DateTimeField action_time
TextField object_id
CharField object_repr
PositiveSmallIntegerField action_flag
TextField change_message
}
EmailAddress{
AutoField id
CharField email
BooleanField verified
BooleanField primary
}
EmailConfirmation{
AutoField id
DateTimeField created
DateTimeField sent
CharField key
}
SocialApp{
AutoField id
CharField provider
CharField name
CharField client_id
CharField secret
CharField key
}
SocialAccount{
AutoField id
CharField provider
CharField uid
DateTimeField last_login
DateTimeField date_joined
TextField extra_data
}
SocialToken{
AutoField id
TextField token
TextField token_secret
DateTimeField expires_at
}
User{
BigAutoField id
CharField password
DateTimeField last_login
BooleanField is_superuser
CharField username
CharField email
BooleanField is_staff
BooleanField is_active
DateTimeField date_joined
CharField name
}
Note{
BigAutoField id
DateTimeField created
DateTimeField updated
CharField name
TextField content
}
Tag{
BigAutoField id
DateTimeField created
DateTimeField updated
CharField name
CharField description
}
Notebook{
BigAutoField id
DateTimeField created
DateTimeField updated
CharField name
TextField description
}
Permission}|--|{Group : group
Permission}|--|{User : user
Permission||--|{ContentType : content_type
Group}|--|{User : user
Group}|--|{Permission : permissions
ContentType||--|{Permission : permission
ContentType||--|{LogEntry : logentry
Site}|--|{SocialApp : socialapp
LogEntry||--|{User : user
LogEntry||--|{ContentType : content_type
EmailAddress||--|{EmailConfirmation : emailconfirmation
EmailAddress||--|{User : user
EmailConfirmation||--|{EmailAddress : email_address
SocialApp||--|{SocialToken : socialtoken
SocialApp}|--|{Site : sites
SocialAccount||--|{SocialToken : socialtoken
SocialAccount||--|{User : user
SocialToken||--|{SocialApp : app
SocialToken||--|{SocialAccount : account
User||--|{LogEntry : logentry
User||--|{EmailAddress : emailaddress
User||--|{SocialAccount : socialaccount
User||--|{Note : note
User||--|{Notebook : book_writer
User}|--|{Group : groups
User}|--|{Permission : user_permissions
Note}|--|{Notebook : booknotes
Note||--|{User : author
Tag}|--|{Notebook : booktags
Notebook||--|{User : author
Notebook}|--|{Note : notes
Notebook}|--|{Tag : tags
```
