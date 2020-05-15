# 0513_Djaogo_pjt4_README

> M:N 관계 기반 팔로우, 좋아요 기능을 갖춘 영화 리뷰 작성 페이지구현 프로젝트
>
> 개발환경 : Python, Django 2.1.15, CS9, Django-bootstrap4

### 1. 구현 과정

#### 0. 프로젝트 시작

1. 페어 프로그래밍으로 진행했기 때문에, 명세서를 함께 읽고 Web을 어떻게 설계할지 충분히 대화를 나누었다.

   - `accounts`, `movies` 두개의 앱을 구성하기로 했다.
   - 어떻게 디자인 할지, 데이터 관계는 어떻게 설정할지, 어떤 추가기능을 구현할지 등에 대해 얘기하며 명세를 구체화했다(현재 미완성 상태, 추후 보완 예정).

2. CS9에 practice/0513 폴더 위치에서 project를 시작해 주었다. (프로젝트명 : django_pjt4)

   ```bash
   django-admin startproject django_pjt4
   ```

3. 이후 practice/0513/django_pjt4에서 `accounts`,`movies` 두 앱을 추가해 주었다.

   ```bash
   python manage.py startapp accounts
   python manage.py startapp movies
   ```

4. settings.py를 아래와 같이 설정해 주었다.

   - ALLOWED_HOSTS = ['*']

   - LANGUAGE_CODE, TIME_ZONE 설정

     ```python
     LANGUAGE_CODE = 'ko-kr'
     TIME_ZONE = 'Asia/Seoul'
     ```

   - TEMPLATES 내 'base.html' 적용을 위한 DIR 설정

     ```python
     'DIRS': [os.path.join(BASE_DIR,'templates')]
     ```

   - INSTALLED_APPS에 앱 추가

     ```python
     'accounts',
     'movies',
     'bootstrap4', # Django-bootstrap4 사용하기 위해
     ```

5. urls.py에 app 경로를 설정해 주었다(include 사용)

   ```python
   from django.contrib import admin
   from django.urls import path, include

   urlpatterns = [
       path('admin/', admin.site.urls),
       path('accounts/', include('accounts.urls')),
       path('movies/', include('movies.urls')),
   ]
   ```

6. templates 폴더를 만들고, `base.html` 파일을 만들었다. 이 때, bootstrap 사용을 위한 코드도 작성해주었다. 세부 내용은  `2. 어려웠던 점 및 배운 점`  참고

7. (05/15) nav바를 설정해주고, 로그인된 계정의 프로필 사진을 nav바 좌측에 보이도록 하였다.

   ```html
   <a class="navbar-brand m-0 p-0" href='{% url "accounts:profile" user.username %}'><img src="{{ user.profile_picture.url }}" style="width:70px; height:80px;" class="p-1 rounded-circle"></a>
   ```



#### 1. `accounts` 앱 구현

> Model -> Form -> URL -> VIEW -> TEMPLATE 순으로 accounts앱을 구현했다.

(지금까지)구현한 내용은 다음과 같다.

- signup, login, logout 기능, 유저의 프로필 페이지, 유저간 팔로우 기능, 프로필 사진 기능(사진 등록이 안되었을 때 기본 이미지 출력 기능 포함)

1. `models.py`

   - profile_picture, followers 기능을 구현하기 위해 AbstractUser에서 상속받은 User라는 객체에 속성값을 추가해주었다.

     ```python
     class User(AbstractUser):
         profile_picture = models.ImageField(blank=True)
         followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'followings')
     ```

     - related_name을 설정해주어 User 클래스 내에서의 충돌을 막아주었다.

   - 이를 프로젝트 내에서 기본 USER 모델로 사용하기 위해 `settings.py`에 다음과 같은 코드를 추가해 주었다.

     ```python
     AUTH_USER_MODEL = 'accounts.User'
     ```

   - 사진을 받아오기 위한 URL,ROOT 설정을 위해 `settings.py`에 다음과 같은 코드를 추가해 주었다.

     ```python
     MEDIA_URL = '/media/'
     MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
     ```

2. `forms.py`

   ```python
   from . import models
   from django.contrib.auth.forms import UserCreationForm
   from django.contrib.auth import get_user_model

   class CustomUserCreationForm(UserCreationForm):
       class Meta:
           model = get_user_model()
           fields = ['username','first_name','last_name','email','profile_picture']
   ```

   - UserCreationForm을 상속받아 Customise된 CreationForm을 생성했다.
     - get_user_model 메서드를 사용하여 자동적으로 프로젝트 내 user_model을 get했다.
     - fields에는 username, password 외에도 다른 필드들을 넣어줬고, 특히 가입 시 프로필사진을 받아오기 위해 profile_picture 필드 또한 추가해 주었다.

3. `urls.py`

   views 내 함수를 불러오기 위한 url들은 다음과 같다.

   ```python
   from django.contrib import admin
   from django.urls import path, include
   from . import views
   ```

   ```python
    app_name = 'accounts'
     urlpatterns = [
        path('',views.index,name='index'),
        path('signup/',views.signup,name='signup'),
        path('login/',views.login,name='login'),
        path('logout/',views.logout,name='logout'),
        path('<username>/', views.profile, name='profile'),
        path('<username>/follow', views.follow, name='follow'),
        ]
   ```

4. `views.py`

   - signup 기능

     - 기본 signup 기능을 POST,GET방식에 따른 form.html 페이지 반환을 통해 구현하였다.

     - 가입 시 이미지 파일을 받아오기 위한 코드를 추가해 주었다. 세부적인 내용은 `2. 어려웠던 점 및 배운 점` 참고

     - 가입 후 자동으로 로그인하도록 기능을 구현하였다.

       ```python
       def signup(request):
           if request.method == 'POST':
               form = CustomUserCreationForm(request.POST,request.FILES)
               if form.is_valid():
                   new_user=form.save()
                   authenticated_user=authenticate(username=new_user.username,password=request.POST['password1'])
                   auth_login(request,authenticated_user)
                   return redirect('accounts:profile', authenticated_user.username)
           else:
               form = CustomUserCreationForm()
           context = {
               'form' : form
           }
           return render(request,'accounts/form.html',context)
       ```

   - login 기능

     - 기본 login 기능을 POST,GET방식에 따른 form.html 페이지 반환을 통해 구현하였다.

     - login 기능을 auth_login으로 불러와 처리해 주었다(재귀를 막기 위해)

     - login이 require되는 페이지에서 접근한 경우, 이후 가려고 했던 페이지로 접근할 수 있도록 하여 사용자의 편의성을 생각하였다.

       ```python
       def login(request):
                  if request.method == 'POST':
                      form = AuthenticationForm(request,request.POST)
                      if form.is_valid():
                          auth_login(request,form.get_user())
                          return redirect(request.GET.get('next') or 'accounts:index')
                  else:
                      form = AuthenticationForm()
                  context = {
                      'form':form
                  }
                  return render(request,'accounts/form.html',context)
       ```

   - logout 기능

     - 기본 logout 기능을 구현하였다.

     - logout 기능을 auth_logout으로 불러와 처리해 주었다(재귀를 막기 위해)

       ```python
         def logout(request):
              auth_logout(request)
              return redirect('accounts:index')
       ```

   - profile 페이지 접근 기능

     - login이 require되도록 decorator를 사용하여 설정해 주었다.

     - profile 사진이 blank일 때 default사진을 처리해주는게 어려워서 여기서 가장 헤맸다. 해결 방법은 `2. 어려웠던 점 및 배운 점` 참고

       ```python
          @login_required
          def profile(request,username):
              User = get_user_model()
              profile_user = User.objects.get(username=username)
              if len(str(profile_user.profile_picture)) == 0:
                  profile_user.profile_picture = 'default_image.png'
                  profile_user.save()

              context = {
                  'profile_user' : profile_user,
              }

              return render(request,'accounts/profile.html',context)
       ```

   - profile 사진 update 기능

     - 해당 사용자가 프로필 페이지에서 본인의 프로필 사진을 누르면 사진을 업데이트 할 수 있도록 구현했다.

       ```python
       def profile_picture_update(request,username):
           user=get_object_or_404(get_user_model() ,username=username)
           if request.method == 'POST':
               form = UpdateProfileForm(request.POST,request.FILES)
               if form.is_valid():
                   new_user = form.save(commit=False)
                   user.profile_picture = new_user.profile_picture
                   user.save()
                   return redirect('accounts:profile',username)
           else:
               form = UpdateProfileForm(instance=user)

           context = {
               'form':form
           }
           return render(request,'accounts/form.html',context)
       ```

    - follow 기능

      - M:N 관계를 이용해서 유저간 follow 기능을 구현하였다.

      - me에는 현재 접속한 user를 할당해 주었고, you에는 해당 페이지의 user를 할당해 주었다.

      - 이후 models.py에서 설정한 followers-followings 관계를 바탕으로 you를 follow하는(followers) queryset 내 me가 있는지 확인해주는 절차를 통해 팔로우, 팔로우 취소 기능을 구현하였다.

        ```python
              @login_required
              def follow(request,username):
                  User = get_user_model()
                  me = request.user
                  you = User.objects.get(username=username)

                  if me in you.followers.all():
                      you.followers.remove(me)
                  else:
                      you.followers.add(me)

                  return redirect('accounts:profile', username)
        ```

  5. Templates

     - `form.html`

       - form을 bootstrap을 이용해서 작성하였다. 세부 내용은  `2. 어려웠던 점 및 배운 점` 참고

       - 프로필 사진을 받아오기 위하여 코드를 추가해 주었다.  `2. 어려웠던 점 및 배운 점` 참고

         ```html
         {% extends 'base.html' %}
                  {% load bootstrap4 %}
                  {% block body %}

                  <form action = '' method ='POST' enctype="multipart/form-data">
                      {% csrf_token %}
                      {% bootstrap_form form %}
                      {% bootstrap_button "제출" button_type="submit" button_class="btn-primary" %}
                  </form>

                  {% endblock %}
         ```

     - `profile.html`

          - profile 페이지 내 사용자 이름, 몇명이 팔로우 하는지, if문을 활용하여 해당 페이지에 접근한 user가 팔로우중이면 팔로우 취소를, 팔로우중이지 않다면 팔로우 할 수 있도록 구성하였다.

          - if문을 활용하여 본인에게는 팔로우 버튼이 보이지 않도록 설정하였다(이 부분 이후 추가 보완 필요. url로 접근할 수 있으니! GET,POST방식 사용해야 할듯? require_POST나)

          - if문을 활용하여 인증된 사용자만 다른 사용자를 팔로우할 수 있도록 구현하였다.

            ```html
                 {% extends 'base.html' %}
                 {% load static %}
                 {% block body %}
                     <img src="{{ profile_user.profile_picture.url }}" class="w-25 rounded-circle">
                     <h1>{{profile_user.username}}님의 Profile</h1>
                     <h1><a>{{profile_user.followers.all|length}}명</a>이 팔로우 합니다.</h1>
                     {% if user.is_authenticated %}
                         {% if user != profile_user %}
                             {% if user in profile_user.followers.all %}
                                 <a href='{% url 'accounts:follow' profile_user.username %}'>팔로우 취소</a>
                             {% else %}
                                 <a href='{% url 'accounts:follow' profile_user.username %}'>팔로우</a>
                             {% endif %}
                         {% endif %}
                     {% endif %}
                 {% endblock %}
            ```



#### 2.  `movies` 앱 구현

- `models.py`

  models.py에는 총 3개의 모델을 구현하였으며

  `movie`와 `review`가 1:n 의 관계, `review`와 `comment`가 1:n, accounts app의 `user`와 `comment`가 1:n, `review`와 `user`가 1:n 그리고 m:n의 관계를 맺는 모델을 구성하였다.

  1:n의 관계의 경우 `on_delete`의 값을 전부 CASCADE 로 설정하였으며 일대다 혹은 다대다 관계에는 모두 `related_name` 을 설정해주었다.

  (review rank)

- `forms.py`

    forms.py에서는 입력 폼을 거의 바꾸지 않고 `models`에서 그대로 가져왔으며 필요한 `fields`만 적절히 수정하였다. (추후에 reviewform rank넣는거 수정 예정)

- `views.py`

    views.py 내부에 정의된 함수는 아래와 같다.

  ```python
  index(request)
  create_movie(request) @login_required
  create_review(request, movie_id) @login_required
  delete_review(request, review_id) @login_required @require_POST
  detail_review(request, review_id)
  ~~update_review(request, review_id)~~ -- 미구현
  create_comment(request, review_id) @login_required @require_POST
  ~~delete_comment(request, comment_id)~~ -- 미구현
  like_review(request, review_id) @login_required
  ```

    `create_movie` 함수에는 함수를 호출한 user가 superuser인지 판단하는 is_superuser함수를 넣었다. 또한 사용자에게서 imagefile을 입력받아 서버 내 media 폴더에 저장하였다. accounts의 user model도 사용자에게서 imagefile을 받아 같은 media 폴더에 넣는 구조라 폴더의 구분이 필요해보였다.

- Templates

    모든 탬플릿들은 bootstrap을 이용해 블럭 바깥을 container로 감싸놓았으며 form.html은 bootstrap4를 사용하여 깔끔한 입력 form을 사용자에게 제공할 수 있다.



### 2. 어려웠던 점 및 배운 점

#### accounts 앱

---

- bootstrap 적용을 처음해 봤는데, 적용 절차가 어려웠다. 배우게 된 점은 다음과 같다.

  - django-bootstrap4 설치(bootstrap4도 설치했었는데, 이 것은 적용이 안됐다.)

    ```bash
    pip install django-bootstrap4
    ```

  - `settings.py` 내 bootsrtap4 앱 추가

  - `base.html` 내 다음 내용 추가

    ```html
    {% load bootstrap4 %} <!--상단-->

    <!--하단, body태그 닫힌 이후-->
    {% bootstrap_javascript jquery='full' %}
    {% bootstrap_css %}
    ```

  - 모든 html 파일 상단에 {% load bootstrap4 %}  삽입 (질문 : base.html에 있는데 왜 다 넣어야할까?)

  - 교수님께 bootstrap 기능을 모두 구현할 수 있냐고 여쭤봤는데, 그렇다고 하셨다. 그러나 기존 class에 추가하는 방식과는 많이 달랐고, 다음과 같이 코드가 표현됐다.

    ```html
    <!--예시-->
    {% bootstrap_form form %}
        {% bootstrap_button "제출" button_type="submit" button_class="btn-primary" %}
    ```

  - 공식 문서 URL 참고 : https://django-bootstrap4.readthedocs.io/en/latest/



- Image 삽입

  - Image 삽입을 배우기만 했고, 적용했던 적은 없어서 매우 어려웠다. 시행착오를 가장 많이 겪은 부분이다. 해결 과정은 다음과 같다.

  - 프로젝트 뎁스에서 media 폴더를 생성해 주었다.

  - `settings.py`'에 다음 내용을 적어주어 MEDIA의 URL, ROOT를 설정해 주었다.

    ```python
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    ```

  - 회원가입 시 파일을 받아오기 위해서는 회원가입 모델폼에 request.FILES라는 값 또한 받아와줘야 했다.

    ```python
    form = CustomUserCreationForm(request.POST,request.FILES)
    ```

  - `urls.py`에 다음과 같은 내용을 작성해주었다. 코드가 각각 무엇을 의미하는지 추후에 보완해야겠다.

    ```python
    from django.conf.urls.static import static
    from django.conf import settings
    # urlpatterns가 닫힌 뒤
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    ```

  - `form.html`에서 form을 보내줄 때 다음과 같이 enctype을 지정해주어야 했다.

    ```html
    <form action = '' method ='POST' enctype="multipart/form-data">
    ```



- Blank vs Null

  - 회원가입시 Image의 NOT_NULL = Yes인데, `blank=True`를 해줬다고 해서 파일 업로드를 하지 않아도 회원가입이 돼서 의심을 갖게 되었다.

  - 나를 가장 힘들게 한 부분이다.. Image를 받아올 때 `blank=True`를 해주었는데, 이 값이 뭔가 아무것도 없는데 null은 또 아니여서 해결하는데 큰 수고가 따랐다. 가입 시 Image를 등록하지 않은 사람(blank로 한 사람) 처리가 어려웠기 때문이다.

  - 해결하기 위해 3가지 방법을 생각해 냈는데, 결국 1,3번으로만 문제를 해결해낼 수 있었다 (추후 2번을 보완해보자).

    1. Profile 함수 내에서 사진을 디폴트 사진을 등록하고 html로 넘어와서 사진을 출력하는게 좋을지

    2. profile_user.profile_picture << 이 안에 디폴트 사진을 저장을 어떻게 할지

       ```python
       # 1,2번을 보완하기 위한 코드
       if len(str(profile_user.profile_picture)) == 0:
               profile_user.profile_picture = 'default_image.png'
               profile_user.save()
       ```

    3. html 페이지에서 if문을 써줘서 처리해주는게 좋을지__(해결 아직 못함)

       - 비어있는지 확인하려고 {% if profile_user.profile_picture == Null %} 라고 썼는데 작동을 안해서, 어떻게 고치면 좋을지



#### movies 앱

----

- ``models.py`` -- 관계 구현하기

  user와 review의 m:n 관계를 구현하며 테이블의 충돌을 경험하였다. 예전에 homework와 quiz로도 나왔던 내용이였지만 당시에는 m:n의 관계를 정확하게 이해하고 있지 못했기 때문에 이번에도 똑같은 실수를 하였다.

  ```python
    # movies.models.Review
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews')

    # accounts.models.User
    like_reviews = models.ManyToManyField(Review, related_name='like_users')
  ```

  처음에는 User에서 m:n으로 생성된 테이블과 Review에서 m:n으로 생성된 테이블이 만나기 위해서는 related_name이 서로 맞물려 있어야 한다고 생각했으며 위와 같이 코드를 작성했지만 충돌이 일어났다. m:n의 개념과 ManyToManyField의 사용법을 좀 더 공부한 뒤에야 m:n을 확실히 이해하게 되었다.

- `views.py`

  create_review 함수를 구현하는 과정에서 오류가 발생하였다.

  ```python
    def create_review(request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        if request.method == "POST":
            form = ReviewForm(request.POST)
            if form.is_valid():
                form.save(commit=False)
                form.movie = movie
                form.user = request.user
                form.save()
                return redirect('movies:index')
  ```

    처음에는 위와 같은 방식으로 코드를 구성하였고 오류가 나게 되었다.

    POST로 받아온 form에 그대로 추가값을 저장하면서 발생하게 된 오류이며 아래의 코드로 변경하여 오류를 잡았다.

  ```python
    review = form.save(commit=False)
    review.movie = movie
    review.user = request.user
    review.save()
    return redirect('movies:index')
  ```

    아마도 .save()함수는 form이 메타정보로 가지고있는 원본 model에 입력받은 data를 집어넣어 return값으로 반환하는 기능을 하는것 같다. 그렇기에 form에 직접 추가값을 저장하였을때는 코드가 작동하지 않았지만 form.save()를 review에 할당하여 값을 저장할때는 제대로 동작 했던 것으로 추측한다.

  ```python
    class ReviewForm(forms.ModelForm):
        class Meta:
            model = Review
            fields = ['title', 'content', 'rank',]
  ```

    ++ 아니면 form 과 form.save()의 반환값 모두 같은 type이지만 form의 fields가 `__all__`이 아니라서 작동을 제대로 하지 않은것인가도 의심된다.

    +++ 같은 문제가 `update_review` 를 구현하는 과정에서도 form.movie 처럼 인자를 건드리는 경우에는 반드시 새로운 변수에 할당을해주고 작업해야 한다. 아니면 오류가 나더라.



- 모델 구성과 on_delete="CASCADE"의 기능에 관해

  모델을 마무리 하며 테스트를 하던 도중 자식을 가지고있는 부모 row 데이터가 삭제되지 않는 문제를 발견했다. on_delete="CASCADE"에 의해 부모가 삭제가 된다면 자식데이터들은 알아서 삭제가 되어야하는데 애초에 자식이 존재하는 부모가 삭제가 되지 않았다. 어째서 이런 오류가 발생하는지는 알수없다.



- image 파일의 sizing

  carousel에 들어갈 영화 포스터사진의 size를 동일하게 맞추는 과정을 진행하였으나 css와 bootstrap를 하며 배웠었던 내용들이 잘 기억나지 않아 서로 비율이 다른 사진들의 size를 맞추는 데에 실패하였고 결국 같은 비율의 영화 포스터사진만을 모아 사이트를 구성하게 되었다. 어려웠다기보다는 분명 할줄 알았는데 지금은 못하게 됐다는 생각이 들어 답답하게 느껴진 부분이였다.




### 3. 추후 보완해낼 점

- ~~회원가입 시 Image 등록하지 않은 사람 Image 추가하기~~
- Login 기능을 bootstrap Modal을 이용해서 구현할 예정 : 아직 기술이...
- Review에서 rank를 입력받을때 현재는 사용자가 직접 int값을 입력하는 형태를 하고있지만 1차적으로 1~10까지의 점수를 사용자가 선택하는 라디오 버튼등의 형식으로 바꿀 것이며 최종적으로는 별점의 형태로 rank값을 입력받고 싶다.
  __부모,자식 데이터간의 삭제문제를 해결하느라 시도조차 하지 못함 ㅠㅠ__
- ![image-20200515180656962](0513_pjt README.assets/image-20200515180656962.png)
  - 회원이 탈퇴하거나 게시글이 삭제되더라도 media폴더에 그대로 남아있는 현상을 발견하였다. 이 부분을 나중에 공부해서 해결해 볼 것이다.
  - 사진을 효율적으로 관리할 수 있는 방법을 발견했다. 지금은 영화등록, 프로필사진 등록 등 모두 한 폴더에서 관리하지만, url을 달리 설정해주면 따로 저장할 수 있는 것을 발견했다. (추후 보완해낼 예정)
- ~~선언만 해두고 아직 구현하지 못한 update_review와 delete_comment 기능을 우선적으로 추가해줘야 한다. 이후에는 아직 선언도 하지 않은 movie의 삭제, 수정을 views에 구현한다.~~ 구현 완료!
- ~~보완 및 추가해야할점의 대부분이 templates에 몰려있다. 일단 bootstrap으로 기본적인 구색만 갖춰놓은 각 탬플릿들의 비쥬얼적인 부분을 전면적으로 수정해야한다. 또한 base.html에 accounts의 index기능을 하는 navbar를 추가하고 index.html에 있는 영화 리스트를 carousel로 변경하여 사이트 전체의 완성 확 끌어올릴 예정이다.(수일 내 추가작업 예정)~~ 구현 완료!





### 4. 느낀점

#### 전석현

- 여태까지 배운 모든 것을 적용한 모든 것, 혹은 그 이상을 쏟아붓기 위해 노력했던 프로젝트였다.
- CRUD, 데이터 관계 설정에 대해서 많이 익숙해질 수 있던 시간이었다.
- __개발이라는게 무엇인지 조금이나마 이해할 수 있게 된 프로젝트였다.__
  - 기존 CRUD, 1:N, M:N 등 방식들을 넘어서, __우리가 무엇을 만들고싶고 그것을 위해서는 무엇이 필요한지 하나하나 검색하고 서로 물어보면서 적용하고, 어려움들을극복해냈다.__
- __바닥부터 하나하나 build-up을 하면서, 개발이 얼마나 어려운지 그리고 사용자 입장에서 생각해보며 user-friendly한 web 구현이 얼마나 어려운지 느낄 수 있었다.__
- 서비스를 개발하고, 배포하여 Feedback을 받고 보완해나가는 개발자로 성장하고 싶다는 생각이 많이 들었던 것 같다. 내가 개발한 것을 국민들이 쓰고, 그 분들에게 피드백을 받아 수정하며 완성도 있는 서비스를 제공하는 개발자가 되고싶다!
- 페어 프로그래밍도 이렇게 재밌고 유익한데, 팀프로젝트를 하게되면 얼마나 많이 배우고 성장할지 정말 궁금하다... 역시 나는 혼자 뭐 하는것 보단 사람들과 함께 하는게 젤 좋은 것 같다.
- '이번 프로젝트 제대로 해보자!' 라는 마음이 진솔이랑 잘 맞아서, 많은 시간을 투자하여 이 프로젝트를 진행할 수 있었고, 앞으로도 이 프로젝트는 쭉 진행될 것이다.
- 다른 팀원과 진행했으면 그냥 한 번의 경험이 될 수 있었던 프로젝트였지만, SSAFY 입과 후 어떤 개발자로 성장하고싶은지, 개발이 무엇인지에 대해서 진지하게 생각하고 배울 수 있었던 소중한 시간이었다. ~~진솔아 고마워~~
- 아직 페이지 구현이 미숙하고, 코드 자체도 비효율적일수도 있지만!! 나중에 이 글을 읽을 때는, 그 땐 그랬지 할 수 있도록 이 프로젝트를 끝까지 밀고나가 볼 것이다!!! 진솔아 고생하자 화이팅!

#### 이진솔

- pair programming을 빡시게 진행해보면서 코딩을 같이하는데서 오는 시너지가 얼마나 큰지를 확실히 느낄 수 있었다.
- 명세에 나와있는 필수 기능부분 의외에도 pair와 함께 의논하여 프로젝트의 완성도를 높이려 노력하였는데 이러한 작업 전반이 매우 재미있었다.
- 웹 초창기에 배웠던 html, css에서부터 django 백엔드의 핵심기능들까지 모든것을 프로젝트에 넣는 과정에서 지금까지 했었던 어떤 프로젝트보다 훨씬 더 실력향상에 도움이 되었다.

- 연일에 걸친 프로젝트내용을 readme로 정리, 수정하며 readme 작성에 대한 중요성을 정말 정말 뼈저리게 느낄수 있었다.
- 프로젝트를 일회성으로 진행하는것보다 이미 완성했던 프로젝트에 수정에 수정을 거치는 편이 코딩실력 향상에 크게 도움 될 것이다. **그니까 앞으로 옛날에 했던 프로젝트들좀 꺼내서 자주 만져보자.**