import api from '@/services/api'

export default {
  fetchMessages() {
    return api.get(`messages/`)
              .then(response => response.data)
  },
  postMessage(payload) {
    return api.post(`messages/`, payload)
              .then(response => response.data)
  },
  deleteMessage(msgId) {
    return api.delete(`messages/${msgId}`)
              .then(response => response.data)
  },
  shit() {
  return api.post(`shit/`)
        .then(response => response.data)
  }
}