<template lang="pug">
    v-card.pa-5(width="600")
        v-container    
            v-row.pb-4
                h2.font-weight-regular.teal--text.darken-1 Please sign-in to proceed
            v-row
                v-tabs.elevation-2(v-model='tab' background-color='teal darken-1' dark grow)
                    v-tab Sign in
                    v-tab Register
                    v-tab-item.pa-3
                        Login
                    v-tab-item.pa-3
                        RegisterForm
</template>
<script>
import Login from './Login'
import RegisterForm from './RegisterForm'
export default {
  name: 'LoginOrRegister',
  components: {
    Login,
    RegisterForm
  },
  data() {
    return {
      tab: null
    }
  }
}
</script>
