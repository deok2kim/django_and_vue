# django for vue
1. ***기본 준비***

2. mkdir django_for_vue

3. cd django_for_vue

4. python -m venv venv

5. 확인) source venv/Scripts/activate, pip list, python -m pip install --upgrade pip

6. touch .gitignore

7. gitignore.io > venv, django, visualstudiocode

8. 복사 후 .gitignore에 붙여넣기

9. 확인) git status | .gitignore만 보임, venv 음영처리

10. source venv/Scripts/activate

11. pip install django==2.1.15 djangorestframework

12. pip freeze > requirements.txt

13. ***프로젝트 시작***

14. django-admin startproject django_for_vue . | . 의 의미는 현재폴더에 생성하기

15. setting.py > installedapp > 'rest_framework' 등록

16. python manage.py startapp accounts

17. python manage.py startapp articles

18. setting.py > installedapp > 'accounts', 'articles' 등록

19. user model을 굳이 변경하지 않더라도 나중에 확장성을 보장해주기 위해

    ```python
    # accouts > models.py
    from django.contrib.auth.models import AbstractUser
    
    class User(AbstractUser):
        pass
    
    
    # settings.py 맨아래
    AUTH_USER_MODEL = 'accounts.User'
    ```

20. articles > models.py 에 모델 정의

21. python manage.py makemigrations, python manage.py migrate | 모델링 끝

22. touch articles/serializers.py

    ```python
    from rest_framework import serializers
    from .models import Article
    
    class ArticleListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Article
            fields = ['id', 'title', 'created_at']
    
    class ArticleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Article
            fields = '__all__'
    ```

    

    

    

## accounts

```bash
pip install django-rest-auth django-allauth
# django-rest-auth는 로그인 로그아웃
# django-allauth는 사인업까지
```

문서는 djanog rest auth



- settings.py

  ```python
  installed apps = [
      #DRF
      'rest_framework.authtoken,' # 토큰베이스로 인증하려면 이거쓰세요
      
      #rest_auth
      'rest_auth'
  ]
  ```

  ```python
  # DRF auth settings.
  REST_FRAMEWORK = {
      'DEFAULT_AUTHENTICATION_CLASSES': [
          'rest_framework.authentication.BasicAuthentication',
          'rest_framework.authentication.SessionAuthentication',
      ]
  }
  
  #우리는 토큰어쎈을 쓸것이기 때문에 위 대신 아래를 써준다
  REST_FRAMEWORK = {
      'DEFAULT_AUTHENTICATION_CLASSES': [
          'rest_framework.authentication.TokenAuthentication',
      ]
  }
  ```

  여기까지 기본 세팅

- urls.py

  ```python
  # rest-auth
  path('rest-auth/', include('rest_auth.urls'))
  ```

- 로그인은 토큰 발급

### signup(allauth)

- settings.py

  ```python
  # installed apps
      'django.contrib.sites', # registraion
  
      # rest-auth + allauth
      'allauth',
      'allauth.account',
      'rest_auth.registration',
  
  # django sites app setting
  SITE_ID = 1
  
  ```

- urls.py

  ```python
  # path('rest-auth/registration/', include('rest_auth.registration.urls'))
  # signup으로 이름 바꿔도 된다.
  path('rest-auth/signup/', include('rest_auth.registration.urls'))
  ```



### user도 serializer를 해야 한다

- articles에 user를 엮기 위해서

- ```bash
  touch accounts/serializers.py
  ```

- accounts/serializers.py

  ```python
  from django.contrib.auth import get_user_model
  from rest_framework import serializers
  
  User = get_user_model()
  
  class UserSerializer(serializers.ModelSerializer):
      class meta:
          model = User
          fields = ['id', 'username']
  ```

- articles/serializers.py

  ```python
  + from accounts.serializers import UserSerializer
  
  class ArticleSerializer(serializers.ModelSerializer):
      + user = UserSerializer()
      class Meta:
          model = Article
          fields = '__all__'
  ```

- 어떻게 serializer.is_valid를 통과할것인가

  ```python
  user = UserSerializer(required=False)
  # is_valid() 에서 유무검증 pass
  ```

- articles/views.py = create_article

  ```python
  serializer.save(user=request.user)
  괄호안에 아무것도 안넣을 경우 # NOT NULL CONSTRAINT FAILED
  ```

  내가 누군지 인증하는것은 헤더에 있다

  headers - Authorization - Token 토큰값

- html에서 쓰는 login_required 대신 쓰는것 permission_classes | views.py

  ```python
  from rest_framework.decorators import permission_classes
  from rest_framework.permissions import IsAuthenticated
  
  @permission_classes([IsAuthenticated])
  ```




## 프론트로 넘어가기

### axios 요청을 보낼 때 headers에 뭔가를 담아서 보내야 한다

```bash
pip install django-cors-headers
```

- settings.py

  ```python
  installed app =[
      # CORS
      'corsheaders',
  ]
  
  middleware = [
      # 순서가 중요함 commonmiddleware보다 위에 써주자
      'corsheaders.middleware.CorsMiddleware',
  ]
  ```

  브라우저야 얘만 열어줘 whitelist

  ```python
  # CORS Allow
  CORS_ORIGIN_ALLOW_ALL = True
  ```

  