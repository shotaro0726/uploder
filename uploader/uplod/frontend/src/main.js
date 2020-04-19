import Vue from 'vue'
import App from './App.vue'
import router from './router'

Vue.config.productionTip = false

const getCookie = name => {
  if (document.cookie && document.cookie !== '') {
    for (const cookie of document.cookie.split(';')) {
      const [key, value] = cookie.trim().split('=')
      if (key === name) {
        return decodeURIComponent(value)
      }
    }
  }
}

Vue.prototype.$csrfToken = getCookie('csrftoken')
Vue.prototype.$http = (url, opts) => fetch(url, opts)
Vue.prototype.$endpoint = 'http//127.0.0.1:8000/uplod/api/composites/'

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')