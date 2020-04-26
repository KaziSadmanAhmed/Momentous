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

  async createWallet(id, fullname) {
    const res = await this.post('user/wallet/' + id, fullname)
    return res
  }

  get(resource, config = {}) {
    return this.$http.$get(resource, config)
  }

  post(resource, data = {}, config = {}) {
    return this.$http.$post(resource, data, config)
  }

  listCauses() {
    return this.get('/causes/list')
  }

  getLeaderboard() {
    return this.get('/users/leaderboard')
  }

  uploadCauseImage(data) {
    const formData = new FormData()
    formData.append('image', data.image)
    const config = {
      headers: {
        'Content-Type': 'multipart/form-dataa',
        'Image-Size': data.image.size
      }
    }
    return this.post(`/cause/asset/images/${data.userId}`, formData, config)
  }

  createCause(data) {
    return this.post(`/cause/create/${data.userId}`, {
      content: data.content,
      images: [data.imageUrl]
    })
  }

  giveVote(data) {
    return this.post(`/cause/vote/${data.userId}/${data.causeId}`, {
      vote: data.voteType,
      SK: data.SK
    })
  }

  getUserWallet(userId) {
    return this.get(`/user/wallet/${userId}`)
  }
}

export default API
