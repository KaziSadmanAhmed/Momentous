<template lang="pug">
  v-form(v-model="valid" @submit.prevent="login()")
    v-text-field(
      v-model="userInfo.email"
      :rules="[required('email'), emailFormat()]"
      color="teal darken-1"
      label="E-mail"
      :loading="isFormLoading"
      :disabled="isFormDisabled")
    v-text-field(
      v-model="userInfo.password" 
      :type="isVisible ? 'text' : 'password'"
      :append-icon="isVisible ? 'mdi-eye' : 'mdi-eye-off'"
      :rules="[required('password'), minLength('Password', 8)]"
      @click:append="isVisible = !isVisible"
      color="teal darken-1"
      label="Password"
      :loading="isFormLoading"
      :disabled="isFormDisabled")
      
    v-checkbox( color="teal darken-1" label="Remember me")
    //- error message for v-alert
    v-alert.pa-1(v-if="errMessage !== ''" outlined='' color='red darken-2')
      p {{errMessage}}
    v-btn.mt-4.white--text( block tile color="teal darken-1" :disabled="!valid" type="submit") Sign In
    //-snackbar  for succeesful login
    v-snackbar(v-model='snackbar' :timeout="timeout" color="teal darken-1") SUCCESSFULLY SIGNED IN!
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
      isVisible: false,
      snackbar: false,
      timeout: 3500,
      isFormLoading: false,
      isFormDisabled: false,
      errMessage: ''
    }
  },
  methods: {
    login() {
      this.isFormLoading = true
      this.isFormDisabled = true
      this.errMessage = ''
      console.log('inserted into the login method ')
      this.$auth
        .login({
          username: this.userInfo.email,
          password: this.userInfo.password
        })
        .then((res) => {
          this.snackbar = true
          this.isFormLoading = false
          this.$router.push({
            name: 'donate'
          })
          console.log('login success !')
        })
        .catch((err) => {
          this.errMessage = err.message
          this.isFormLoading = false
          this.isFormDisabled = false
          console.log(err)
        })
    }
  }
}
</script>
<style scoped></style>
