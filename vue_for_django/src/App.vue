<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link :to="{ name: 'Login' }">Login</router-link> |
      <router-link @click.native="logout" to="/accounts/logout">Logout</router-link>
    </div>
    <router-view @submit-login-data="login" />
  </div>
</template>

<script>
import axios from 'axios'

const SERVER_URL = 'http://localhost:8000'

export default {
  name: "App",
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
    login(loginData) {
      axios.post(SERVER_URL + '/rest-auth/login/', loginData)
        .then(res => {
          this.setCookie(res.data.key)
          this.$router.push({ name:'Home' })
        })
        .catch(err => console.log(err.response))
    },
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
        .catch(err => console.log(err.response.data))
    }
  },
  mounted() {
    this.isLoggedIn = this.$cookies.isKey('auth-token')
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
