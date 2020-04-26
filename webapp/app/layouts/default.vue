<template lang="pug">
  v-app
    v-app-bar(color="primary" app)
      v-app-bar-nav-icon(dark @click="drawer = !drawer")
      v-toolbar-items
        v-btn(text dark)
          v-toolbar-title Momentous

    v-navigation-drawer(v-model="drawer" color="primary" fixed app dark)
      v-container
        v-row.py-12(justify="center")
          h2.display-1.white--text Momentous
          p.white--text Coins for the community!
      v-divider
      v-container
        v-list(dense nav class="py-0")
          v-list-item-group
            v-list-item(v-for="link in sidebarLinks" :key="link.title" link :to="{name: link.name}")
              v-list-item-content
                v-list-item-title
                    h3.text-center {{ link.title }}

      template(v-slot:append)
        div.pa-2.mb-5.mb-md-12
          v-btn(outlined block color="white" @click="openRegisterModal = !openRegisterModal") Join
      v-dialog(width="550" v-model="openRegisterModal")
        LoginOrRegister

    v-content
      v-container
        nuxt
</template>
<script>
import LoginOrRegister from '../components/loginOrRegister'
export default {
  components: {
    LoginOrRegister
  },
  data() {
    return {
      drawer: true,
      openRegisterModal: false,
      sidebarLinks: [
        { title: 'Donate', name: 'donate' },
        { title: 'Leaderboard', name: 'leaderboard' },
        { title: 'Cause Wall', name: 'causewall' }
      ]
    }
  }
}
</script>
