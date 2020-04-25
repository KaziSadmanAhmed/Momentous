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

  async createWallet(id) {
    const res = await this.post('user/wallet/' + id)
    return res
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
}

export default API
