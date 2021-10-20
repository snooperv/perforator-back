import { HTTP } from './common'
export const User = {
  create: function (config) {
    return HTTP.post('/users/', config)
      .then(response => {
        return response.data
      })
  },
  delete (note) {
    return HTTP.delete(`/users/${note.id}/`)
  },
  list () {
    return HTTP.get('/users/').then(response => {
      return response.data
    })
  }
}
