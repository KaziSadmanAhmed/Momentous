<template lang="pug">
  section#Register
    v-form.pa-3(v-model="valid" @submit.prevent="register()")
      v-text-field(
        v-model="userInfo.givenName"
        :rules="[required('First name')]"
        color="teal darken-1"
        label="First Name"
        :loading="isFormLoading"
        :disabled="isFormDisabled")
      v-text-field(
        v-model="userInfo.familyName" 
        :rules="[required('Last name')]"
        color="teal darken-1"
        label="Last Name"
        :loading="isFormLoading"
        :disabled="isFormDisabled")
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
        
      v-text-field(
        v-model="userInfo.confirmPassword" 
        :type="isVisible ? 'text' : 'password'"
        :append-icon="isVisible ? 'mdi-eye' : 'mdi-eye-off'"
        :rules="[required('password'), minLength('Password', 8), matchPassword(userInfo.password)]"
        @click:append="isVisible = !isVisible"
        color="teal darken-1"
        label="Confirm Password"
        :loading="isFormLoading"
        :disabled="isFormDisabled")
      //- error message box
      v-alert.pa-1(v-if="errMessage !== ''" outlined='' color='red darken-2')
        p {{errMessage}}  
        
      v-btn.mt-4.white--text(block tile color="teal darken-1" :disabled="!valid" type="submit") Register
    
    v-dialog(v-model="verificationDialog" max-width="250px")
        v-card
          v-container
            v-form(v-model="validVerification" @submit.prevent="confirmRegistration()")
              v-text-field(
                v-model="verificationCode" 
                label="Enter Verification Code" 
                :rules="[required('Verification Code')]"
                :loading="isVerificationFormLoading"
                )
              v-btn.white--text(block tile color="teal darken-1" :disabled="!validVerification" type="submit") Verify
    //-snackbar for registration
    v-snackbar(v-model='snackbar' :timeout="timeout" color="teal darken-1") SUCCESSFULLY REGISTERED!
</template>
<script>
import validations from '../utilities/validations'
export default {
  name: 'RegisterForm',
  data() {
    return {
      valid: false,
      validVerification: false,
      verificationDialog: false,
      verificationCode: '',
      userInfo: {
        email: '',
        password: '',
        confirmPassword: '',
        givenName: '',
        familyName: ''
      },
      ...validations,
      isVisible: false,
      snackbar: false,
      timeout: 3500,
      isFormLoading: false,
      isFormDisabled: false,
      isVerificationFormLoading: false,
      errMessage: ''
    }
  },
  // computed: {
  //   user() {
  //     return this.$auth.getUser()
  //   }
  // },
  computed: {
    openJoinDialog: {
      get() {
        return this.$store.getters['auth/getJoinDialog']
      },

      set() {
        return this.$store.commit('auth/setJoinDialog', false)
      }
    }
  },
  methods: {
    login() {
      return this.$auth
        .login({
          username: this.userInfo.email,
          password: this.userInfo.password
        })
        .then((res) => {
          console.log('Logged In')
        })
        .catch((err) => console.log(err))
    },
    register() {
      this.errMessage = ''
      this.isFormLoading = true
      this.isFormDisabled = true
      this.$auth
        .register({
          username: this.userInfo.email,
          password: this.userInfo.password,
          attributes: {
            given_name: this.userInfo.givenName,
            family_name: this.userInfo.familyName
          }
        })
        .then(() => {
          this.isFormLoading = false
          this.verificationDialog = true
          console.log('register success!')
        })
        .catch((err) => {
          this.errMessage = err.message
          this.isFormLoading = false
          this.isFormDisabled = false
          console.log('error', err)
        })
    },
    confirmRegistration() {
      this.isVerificationFormLoading = true
      this.$auth
        .confirmRegistration({
          username: this.userInfo.email,
          code: this.verificationCode
        })
        .then(async (res) => {
          this.isVerificationFormLoading = false
          await this.login()
          const user = await this.$auth.getUser()
          const fullname =
            this.userInfo.givenName + ' ' + this.userInfo.familyName
          console.log(user)
          console.log(user.sub)
          await this.$api.createWallet(user.sub, { user_name: fullname })
          this.snackbar = true
          this.verificationDialog = false
          this.$store.commit('auth/setJoinDialog', false)
          this.$router.push({
            name: 'donate'
          })
        })
        .catch((err) => {
          this.isVerificationFormLoading = true
          console.log(err)
        })
    }
  }
}
</script>
<style scoped></style>
