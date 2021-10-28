import axios from 'axios'
export const HTTP = axios.create({
  baseURL: 'http://' + location.hostname + ':8000/api/v2/'
})
