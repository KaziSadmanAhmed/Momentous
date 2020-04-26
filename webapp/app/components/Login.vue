<template lang="pug">
  v-form(v-model="valid" @submit.prevent="login()")
    v-text-field(v-model="userInfo.email"
      :rules="[required('email'), emailFormat()]"
      color="teal darken-1"
      label="E-mail")

    v-text-field(v-model="userInfo.password" :type="isVisible ? 'text' : 'password'"
      :append-icon="isVisible ? 'mdi-eye' : 'mdi-eye-off'"
      :rules="[required('password'), minLength('Password', 8)]"
      @click:append="isVisible = !isVisible"
      color="teal darken-1"
      label="Password")
      

    v-checkbox( color="teal darken-1" label="Remember me")
    v-btn.mt-4.white--text( block tile color="teal darken-1" :disabled="!valid" type="submit") Sign In

    //- <nuxt-link to="/dashboard">
    //-   v-btn.mt-4.white--text( block tile color="teal darken-1" :disabled="!valid" type="submit") Sign In
    //- </nuxt-link>
</template>

<script>
import validations from '../utilities/validations'
export default {
  name: 'RegisterForm',
  data() {
    return {
      ...validations,
      userInfo: {
        email: '',
        password: ''
      },
      valid: false,
      isVisible: false
    }
  },
  methods: {
    login() {
      // this.loading = true
      console.log('inserted into the login method ')
      this.$auth
        .login({
          username: this.userInfo.email,
          password: this.userInfo.password
        })
        .then((res) => {
          // this.loading = false
          // this.$store.commit('setSnackbar', true)
          console.log('login success !')
        })
        .catch((err) => {
          console.log(err)
          // this.btnDisable = false
          // this.loading = false
          // this.errorMsg = err.message
          // this.error = true
        })
    }
  }
}
</script>

<style scoped></style>
