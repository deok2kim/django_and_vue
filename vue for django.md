# vue for django

### 시작하기

```bash
vue create vue_for_django
cd vue_for_django
vue add router

npm run serve # test
```

django 와 vue 의 접점: api (통신 할 수 있는 것)

```bash
npm i axios
```

- App
  - Home - /
  - Login - /login
  - Signup - /signup
  - ArticleList - /articles
  - ArticleDetail - /articles/#



컴포넌트들을 만들고 시작

```bash
cd src/views/
touch LoginView.vue SignupView.vue CreateView.vue ListView.vue
mkdir accounts articles
# 컴포넌트를 폴더 별로 정리가 가능하다
```

최상단에서 로그인 로직을 수행

```javascript
data() {
    return {
        username: null,
        password: null,
    }
}
// 이것보단

data() {
    return {
        loginData: {
            username: null,
            password: null,
        }
    }
}
// 이렇게 객체화 하자
```



데이터를 받아서 axios로 장고로 쏴준다!!

import axios from 'axios'

주소는 http://localhost:8000/rest-auth/login/, loginData를 같이 보낸다

```javascript
methods: {
    login(loginData) {
      axios.post('http://localhost:8000/rest-auth/login/', loginData)
        .then(res => console.log(res.data))
        .catch(err => console.log(err.response))
    }
  }
```

키값이 발급됨 res.data 는 key: ''

이제 발급받은 토큰을 어떻게 처리해야 할까

포스트맨에서는 토큰값을 헤더에 autho...에 붙여서 사용했다

새로고침하면 없어지므로 토큰값을 물리적으로 저장해서 사용해야 한다 - 쿠키에 저장(vue cookies)

```bash
npm i vue-cookies
```

main.js - 뷰에서 전부 뷰쿠키를 사용가능

```javascript
import VueCookies from 'vue-cookies'

Vue.use(VueCookies)
```

다시 쿠키 저장 추가

```javascript
methods: {
    setCookie(token) {
      this.$cookies.set('auth-token', token)  
    },
    login(loginData) {
      axios.post('http://localhost:8000/rest-auth/login/', loginData)
        .then(res => {
          this.setCookie(res.data.key)
          // 로그인이 끝나면 홈으로 보내기
          this.$router.push({ name: 'Home' })
      })
        .catch(err => console.log(err.response))
    }
  }
```

로그인 - 토큰발급받아서 토큰저장

로그인 플래그 추가

```javascript
data() {
    return {
        isLoggedIn: false,
    }
},
methods: {
    setCookie(token) {
      this.$cookies.set('auth-token', token)
      this.isLoggedIn = true
    },
    

```



### 로그아웃

포스트 - 헤더에 토큰만 잘

여기서는 쿠키에 있는 토큰을 지우자 | 토큰을 헤더에 담아 보내주면서

axios.post(URL, BODY, HEADER)

```javascript
const SERVER_URL = 'http://localhost:8000'

logout() {
    const requestHeaders = {
        headers: {
            'Authorization': `Token ${this.$cookies.get('auth-token')}`
        }
    }
    axios.post(SERVER_URL + '/rest-auth/logout/', null, requestHeaders)
      .then(() => {
        this.$cookies.remove('auth-token')
        this.isLoggedIn = false
        this.$router.push('/')
    })
      .then(err => console.log(err.response.data))
}
```

사용자에게 로그아웃 주소보여주기

```html
<router-link to="/accounts/logout">Logout</router-link>

```

컴포넌트는 일반적으로 아래에서 오는 메시지를 듣는다.

하지만 click.native 옵션을 추가하면 일반적인 클릭처럼 사용할 수 있다.



mounted에서 ( 자동으로 이 시점에 실행하는 코드)

cookie 에 auth-token 이 존재하는지 체크

```javascript
mounted() {
    // 삼항 연산자
    // this.isLoggedIn = this.$cookies.isKey('auth-token') ? true : false
    this.isLoggedIn = this.$cookies.isKey('auth-token')
    // if (this.$cookies.isKey('auth-token')) {
    //     this.isLoggedIn = true
    // } else {
    //     this.isLoggedIn = false
    // }
},
```

