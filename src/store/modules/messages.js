import messageService from '../../services/messageService'

const state = {
  messages: [],
  shit: false
}

const getters = {
  messages: state => {
    return state.messages
  },
  shit: state => {
    return state.shit
  }
}

const actions = {
  getMessages ({ commit }) {
    messageService.fetchMessages()
    .then(messages => {
      commit('setMessages', messages)
    })
  },
  addMessage({ commit }, message) {
    messageService.postMessage(message)
    .then(() => {
      commit('addMessage', message)
    })
  },
  deleteMessage( { commit }, msgId) {
    messageService.deleteMessage(msgId)
    commit('deleteMessage', msgId)
  },
  vshit({ commit }) {
    messageService.shit()
        .then(velikiy_shit => {
          commit('shit', velikiy_shit)
        })
  }
}

const mutations = {
  setMessages (state, messages) {
    state.messages = messages
  },
  addMessage(state, message) {
    state.messages.push(message)
  },
  deleteMessage(state, msgId) {
    state.messages = state.messages.filter(obj => obj.pk !== msgId)
  },
  shit(state, velikiy_shit) {
    state.shit = true
    alert(velikiy_shit)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}