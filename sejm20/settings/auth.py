AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'allauth.account.auth_backends.AuthenticationBackend',
)
LOGIN_REDIRECT_URL = "/uzytkownik/"

SOCIALACCOUNT_AUTO_SIGNUP = False
SOCIALACCOUNT_QUERY_EMAIL = False

EMAIL_CONFIRMATION_DAYS = 3

