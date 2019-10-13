import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Login from '@/components/Login'
import Logout from '@/components/Logout'
// import Register from '@/components/Register'

Vue.use(Router)



export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld,
      meta: {
        requiresAuth: true
      }
    },
    // {
    //   path: '/register',
    //   name: 'Register',
    //   component: Register,
    //   meta: {
    //     requiresLogged: true
    //   }
    // },
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: {
        requiresLogged: true
      }
    },
    {
      path: '/logout',
      name: 'Logout',
      component: Logout,
      meta: {
        requiresAuth: true
      }
    }
  ]
})
