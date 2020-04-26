<template lang="pug">
  section#Register
    v-form.pa-3(v-model="valid" @submit.prevent="register()")
      v-text-field(v-model="userInfo.givenName" :rules="[required('First name')]"
        color="teal darken-1"
        label="First Name")
      v-text-field( v-model="userInfo.familyName" :rules="[required('Last name')]"
        color="teal darken-1"
        label="Last Name")
      v-text-field(v-model="userInfo.email" :rules="[required('email'), emailFormat()]"
        color="teal darken-1"
        label="E-mail")
        
      v-text-field(v-model="userInfo.password" :type="isVisible ? 'text' : 'password'"
        :append-icon="isVisible ? 'mdi-eye' : 'mdi-eye-off'"
        :rules="[required('password'), minLength('Password', 8)]"
        @click:append="isVisible = !isVisible"
        color="teal darken-1"
        label="Password")
        
      v-text-field(v-model="userInfo.confirmPassword" :type="isVisible ? 'text' : 'password'"
        :append-icon="isVisible ? 'mdi-eye' : 'mdi-eye-off'"
        :rules="[required('password'), minLength('Password', 8), matchPassword(userInfo.password)]"
        @click:append="isVisible = !isVisible"
        color="teal darken-1"
        label="Confirm Password")
        
      v-btn.mt-4.white--text(block tile color="teal darken-1" :disabled="!valid" type="submit") Register
    
    v-dialog(v-model="verificationDialog" max-width="250px")
        v-card
          v-container
            v-form(v-model="validVerification" @submit.prevent="confirmRegistration()")
              v-text-field(v-model="verificationCode" label="Enter Verification Code" :rules="[required('Verification Code')]")
              v-btn.white--text(block tile color="teal darken-1" :disabled="!validVerification" type="submit") Verify

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
      isVisible: false
    }
  },
  // computed: {
  //   user() {
  //     return this.$auth.getUser()
  //   }
  // },
  methods: {
    login() {
      return this.$auth
        .login({
          username: this.userInfo.email,
          password: this.userInfo.password
        })
        .then((res) => {
          console.log('Logged In')
          // this.verifyLoading = false
        })
        .catch((err) => console.log(err))
    },
    register() {
      // this.isRegistered = true
      // this.loading = true
      // this.btnDisable = true
      this.$auth
        .register({
          username: this.userInfo.email,
          password: this.userInfo.password,
          attributes: {
            given_name: this.userInfo.givenName,
            family_name: this.userInfo.familyName
            // 'custom:bill_name': 'my billing name'
          }
        })
        .then(() => {
          // this.isRegistered = false
          // this.loading = false
          // this.btnDisable = false
          this.verificationDialog = true
          console.log('register success!')

          // console.log('Account created. Check your email for verification')
          // this.$router.push(`/auth/verification?email=${userInfo.email}`)
        })
        .catch((err) => {
          // this.isRegistered = false
          // this.btnDisable = false
          // this.loading = false
          console.log(err)
          // this.error = true
          // this.errorMsg = err.message
        })
    },
    confirmRegistration() {
      // this.verifyLoading = true
      this.$auth
        .confirmRegistration({
          username: this.userInfo.email,
          code: this.verificationCode
        })
        .then(async (res) => {
          await this.login()
          const user = await this.$auth.getUser()
          const fullname =
            this.userInfo.givenName + ' ' + this.userInfo.familyName
          console.log(user)
          console.log(user.sub)
          await this.$api.createWallet(user.sub, { user_name: fullname })
          // this.$store.commit('setSnackbar', true)
        })
        .catch((err) => console.log(err))
    }
  }
}
</script>

<style scoped></style>
