import { HTTP } from './common'
export const User = {
  create: function (config) {
    return HTTP.post('/auth/', config)
      .then(response => {
        return response.data
      })
  },
  delete (note) {
    return HTTP.delete(`/users/${note.id}/`)
  },
  list (token) {
    return HTTP.get('/current/', token).then(response => {
      return response.data
    })
  }
}
