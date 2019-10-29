import Vue from 'vue'
import Vuex from 'vuex'
import { axiosBase } from './api/axios-base'

Vue.use(Vuex)

export const store = new Vuex.Store({
  state: {
    accessToken: localStorage.getItem('access_token') || null,

    refreshToken: localStorage.getItem('refresh_token') || null,

    APIData: ''
  },

  getters: {
    loggedIn (state) {
      return state.accessToken != null
    }
  },

  mutations: {
    destroyToken (state) {
      localStorage.removeItem('access_token');
      state.accessToken = null;
    },

    retrieveToken (state, token) {
      localStorage.setItem('access_token', token);
      state.accessToken = token;
    }
  },

  actions: {
    logoutUser (context) {
      context.commit('destroyToken')
    },

    loginUser (context, credentials) {
      return new Promise ((resolve, reject) => {
        axiosBase.post('/file2/auth/login/', {
          username: credentials.username,
          password: credentials.password
        })
          .then(response => {
            const token = response.data.token;
            context.commit('retrieveToken', token);
            resolve(response);
          })
          .catch(error => {
            console.log(error);
            reject(error)
          })
      })
    },

    registerUser (context, credentials) {
      return new Promise ((resolve, reject) => {
        axiosBase.post('/file2/auth/register/', {
          username: credentials.username,
          password: credentials.password,
          email: credentials.email
        })
          .then(response => {
            const token = response.data.token;
            context.commit('retrieveToken', token);
            resolve(response);
          })
          .catch(error => {
            console.log(error);
            reject(error)
          })
      })
    }

  },
})
