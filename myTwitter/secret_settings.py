SECRET_KEY = 'v%)oxsr2%b2qi28i+fxi^6=k&!it_trvbwzzjyx*1t!i(y4!%s'

DATABASES = {
    'default': {
        'HOST': '127.0.0.1',
        'NAME': 'myTwitter',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'root',
        'PASSWORD': 'coderslab',
        'OPTIONS': {
                    'autocommit': True,
        },
    }
}