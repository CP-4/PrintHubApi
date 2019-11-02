// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import {
  store
} from './store'

Vue.config.productionTip = false


router.beforeEach((to, from, next) => {
  console.log('loggedIn: ' + store.getters.loggedIn);
  console.log('accessToken: ' + store.state.accessToken);
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.getters.loggedIn) {
      next({
        name: 'Login'
      })
    } else {
      next()
    }
  } else if (to.matched.some(record => record.meta.requiresLogged)) {
    if (store.getters.loggedIn) {
      next({
        name: 'HelloWorld'
      })
    } else {
      next()
    }
  } else {
    next()
  }
})



/* eslint-disable no-new */
new Vue({
  el: '#app',
  router: router,
  store: store,
  components: {
    App
  },
  template: '<App/>'
})
