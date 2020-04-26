const getUserWallet = (store) => {
  store.subscribe(async (mutation, state) => {
    if (mutation.type === 'auth/setUser') {
      const userId = mutation.payload.sub
      const wallet = await store.$api.getUserWallet(userId)
      store.commit('wallet/setWallet', wallet)
    }
  })
}

export const plugins = [getUserWallet]
