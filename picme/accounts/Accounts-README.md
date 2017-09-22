# View API



# You need to set email address in your settings.py
change EMAIL_BACKEND from
'django.core.mail.backends.dummy.EmailBackend'
to
'django.core.mail.backends.smtp.EmailBackend'



# Templates
1. signin_form.html
2. signup_form.html
3. profile_base.html(other profile page extends this)
4. profile_detail.html
5. profile_form.html
6. email_form.html
7. email_change_complete.html
8. email_confirm.html
9. emails/confirmation_email_message_new.html
10. emails/confirmation_email_message_new.txt
11. emails/confirmation_subject_message_new.html
12. emails/confirmation_subject_message_new.txt
13. password_form.html
14. password_complete.html
15. emails/password_reset_message.html
16. emails/password_reset_message.txt
17. password_reset_form.html
18. password_reset_confirm_form.html


# Urls
1. signin
    accounts/signin/
2. signup
    accounts/signup/
3. user profile
    accounts/[username]
4. edit profile
	accounts/[username]/edit
5. edit email
	accounts/[username]/email
6. edit password
	accounts/[username]/password


# To complete
1. When deployed on cloud, we need to change the domain in template/emails



# Userena 
Userena url.py: https://github.com/bread-and-pepper/django-userena/blob/master/userena/urls.py

Userena Templates: https://github.com/bread-and-pepper/django-userena/tree/master/userena/templates/userena

# Reference
1. [Font Awsome](http://fontawesome.io/ "Font Awsome")
2. [CSS Image size, how to fill, not stretch?](http://stackoverflow.com/questions/11757537/css-image-size-how-to-fill-not-stretch "CSS Image size, how to fill, not stretch?")