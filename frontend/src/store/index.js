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
  users: [], // список заметок
  token: ''
}
// Геттеры
const getters = {
  users: state => state.users // получаем список заметок из состояния
}
// Мутации
const mutations = {
  // Добавляем заметку в список
  [ADD_USER] (state, note) {
    state.users = [note, ...state.users]
  },
  // Убираем заметку из списка
  [REMOVE_USER] (state, { id }) {
    state.users = state.users.filter(note => {
      return note.id !== id
    })
  },
  // Задаем список заметок
  [SET_USER] (state, { notes }) {
    state.users = notes
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
  getUsers ({ commit }, token) {
    User.list(token).then(notes => {
      commit(SET_USER, { notes })
    })
  }
}
export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations
})
