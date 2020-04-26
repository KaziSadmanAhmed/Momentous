<template lang="pug">
  v-app
    <!-- navigation drawer of this app -->
    v-navigation-drawer(v-model="drawer" color="teal darken-1" :right="right" :clipped="clipped" fixed app dark)
      v-container
        v-row(v-if="isAuthenticated" align="center" justify="center") 
          v-avatar(size="150")
            v-img(:src="profile")
        v-row.py-12(v-else justify="center")
          h2.display-1.white--text Momentous   
          p.white--text Cryptocurrency in good use
        v-row.pt-3(align="center" justify="center")
          h3.white--text.text-center {{userName}}
        v-row(align="center" justify="center")
          p.white--text.text-center {{userEmail}}
      v-divider
      v-container
        v-list(dense nav class="py-0")
          v-list-item-group(v-model="selected")
            v-list-item(v-for="item in items" :key="item.title" link :to="item.path")
              v-list-item-content
                v-list-item-title
                    h3.text-center {{ item.title }}
      <!-- logout button -->
      template(v-slot:append)
        div.pa-2.mb-5.mb-md-12
          v-btn(v-if="isAuthenticated" outlined block color="white" @click="signOut") Sign out
          v-btn(v-else outlined block color="white" @click="openRegisterModal = !openRegisterModal") Register
      v-dialog(width="550" v-model="openRegisterModal")
        LoginOrRegister
      //-if user is not registered
      //- v-dialog(width="500" v-model="openRegisterModal")
      //-   v-card(width="500")
      //-     v-container
      //-       v-row( no-gutters)
      //-         h2.px-5.pt-5.headline Register
      //-       v-row(no-gutters)
      //-         v-container
      //-           RegisterForm
    <!-- Content of this app   -->
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
      openRegisterModal: false,
      isAuthenticated: false,
      userName: '',
      userEmail: '',
      drawer: true,
      profile: require('../assets/img/ironMan.jpeg'),
      item: 0,
      items: [
        { title: 'Donate', path: '/donate' },
        { title: 'Leaderboard', path: '/leaderboard' },
        { title: 'Cause Wall', path: '/causewall' }
      ],
      right: false,
      miniVariant: false,
      clipped: false,
      selected: 1
    }
  },
  created() {
    if (this.$auth.isAuthenticated()) {
      this.isAuthenticated = true
      const user = this.$auth.getUser()
      this.userName = `${user.given_name} ${user.family_name}`
      this.userEmail = `${user.email}`
    }
  },
  methods: {
    signOut() {
      this.$auth.logout()
    }
  }
}
</script>
