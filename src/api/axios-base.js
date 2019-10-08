import axios from 'axios'
import store from '../store'

const APIUrl = 'http://127.0.0.1:8000'

const axiosBase = axios.create({
  baseURL: APIUrl,
  // headers: { contentType: 'application/json' }
})

export { axiosBase }
