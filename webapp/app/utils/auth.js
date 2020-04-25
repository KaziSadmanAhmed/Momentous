let AmplifyAuth = null
let store = null

class Auth {
  constructor(option) {
    AmplifyAuth = option.amplifyAuth
    store = option.store
  }

  isAuthenticated() {
    const session = this.getSession()
    if (!session) return false
    const accessToken = session.accessToken
    if (!accessToken) return false
    const hasToken = accessToken.jwtToken
    const isActive = new Date(accessToken.payload.exp * 1000) > new Date()
    const isMe =
      accessToken.payload.username === store.getters['auth/getUser'].username
    return hasToken && isActive && isMe
  }

  fetchUser() {
    return AmplifyAuth.currentAuthenticatedUser({ bypassCache: true }).then(
      (user) => {
        this.setUser(user)
        return user
      }
    )
  }

  getUser() {
    return store.getters['auth/getUser']
  }

  setUser(user = {}) {
    store.commit('auth/setUser', {
      ...{ username: user.username },
      ...user.attributes
    })
  }

  fetchSession() {
    return AmplifyAuth.currentSession().then((session) => {
      return AmplifyAuth.currentUserPoolUser({ bypassCache: true }).then(
        (user) => {
          this.setUser(user)
          this.setSession(session)
          store.$api.setToken(this.getAccessToken())
          return session
        }
      )
    })
  }

  getSession() {
    return store.getters['auth/getSession']
  }

  setSession(session = {}) {
    store.commit('auth/setSession', session)
  }

  getAccessToken() {
    return this.getSession()
      .getAccessToken()
      .getJwtToken()
  }

  register(credentials) {
    return AmplifyAuth.signUp({
      username: credentials.username,
      password: credentials.password,
      attributes: credentials.attributes
    }).then((user) => {
      this.setUser(user)
      return user
    })
  }

  confirmRegistration(data) {
    return AmplifyAuth.confirmSignUp(data.username, data.code)
  }

  resendConfirmation(data) {
    return AmplifyAuth.resendSignUp(data.username)
  }

  forgotPassword(data) {
    return AmplifyAuth.forgotPassword(data.username)
  }

  changePassword(data) {
    return AmplifyAuth.forgotPasswordSubmit(
      data.username,
      data.code,
      data.password
    )
  }

  login(credentials) {
    return AmplifyAuth.signIn({
      username: credentials.username,
      password: credentials.password
    }).then((user) => {
      this.setSession(user.signInUserSession)
      this.setUser(user)
      // store.$api.setToken(this.getAccessToken())
      return user
    })
  }

  logout() {
    if (!this.isAuthenticated()) {
      throw new Error('User not logged in.')
    }

    return AmplifyAuth.signOut().then((res) => {
      this.setUser()
      this.setSession()
      store.$router.push('/')
      return res
    })
  }

  federatedLogin(options = {}) {
    return AmplifyAuth.federatedSignIn({
      provider: options.provider || 'COGNITO'
    })
  }
}

export default Auth
