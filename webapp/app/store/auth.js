export const state = () => ({
  user: {},
  session: {},
  joinDialog: false
})

export const getters = {
  getUser: (state) => state.user,
  getSession: (state) => state.session,
  getJoinDialog: (state) => state.joinDialog
}

export const mutations = {
  setUser: (state, user) => (state.user = user),
  setSession: (state, session) => (state.session = session),
  setJoinDialog: (state, joinDialog) => (state.joinDialog = joinDialog)
}
