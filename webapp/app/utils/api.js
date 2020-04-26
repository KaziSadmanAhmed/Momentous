class API {
  constructor(options) {
    this.$http = options.http
  }

  setToken(token, type = null, scopes = 'common') {
    this.$http.setToken(token, type, scopes)
  }

  clearToken() {
    this.setToken(false)
  }

  get(resource, params = {}) {
    return this.$http.$get(resource, {
      params
    })
  }

  post(resource, data = {}, params = {}) {
    return this.$http.$post(resource, data, {
      params
    })
  }

  listCauses() {
    return this.get('/causes/list')
  }

  getLeaderboard() {
    return this.get('/users/leaderboard')
  }
}

export default API
