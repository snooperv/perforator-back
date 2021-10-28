import axios from 'axios'
export const HTTP = axios.create({
  baseURL: location.hostname + ':8000/api/v2/'
})
