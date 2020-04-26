export const state = () => ({
  wallet: {}
})

export const getters = {
  getWallet: (state) => state.wallet
}

export const mutations = {
  setWallet: (state, wallet) => (state.wallet = wallet)
}
