import Vue from 'vue'
import Vuex from 'vuex'
import { User } from '../api/users'
import {
  ADD_USER,
  REMOVE_USER,
  SET_USER
} from './mutation-types.js'
Vue.use(Vuex)
// Состояние
const state = {
  user: ''
}
// Геттеры
const getters = {
  user: state => state.user // получаем список заметок из состояния
}
// Мутации
const mutations = {
  // Добавляем заметку в список
  [ADD_USER] (state, user) {
    state.user = user
  },
  // Убираем заметку из списка
  [REMOVE_USER] (state, { id }) {
    state.users = state.users.filter(note => {
      return note.id !== id
    })
  },
  // Задаем список заметок
  [SET_USER] (state, { user }) {
    console.log('SET_USER: user = ' + user)
    state.user = user
  }
}
// Действия
const actions = {
  createUser ({ commit }, noteData) {
    User.create(noteData).then(note => {
      commit(ADD_USER, note)
    })
  },
  deleteUser ({ commit }, note) {
    User.delete(note).then(response => {
      commit(REMOVE_USER, note)
    })
  },
  getCurrentUser ({ commit }) {
    User.current().then(user => {
      commit(SET_USER, { user })
    })
  },
  loginUser ({ commit }, payload) {
    User.login(payload).then(user => {
      commit(SET_USER, { user })
    })
  }
}
export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations
})
