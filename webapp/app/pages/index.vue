<template lang="pug">
  v-layout.mt-12( column justify-center align-center)
    v-container.justify-start.mt-md-12
      v-card.mx-auto.my-12(max-width="1000")
        v-container
          v-row(justify="space-between")
            v-col(cols="12" md="7")
              v-container.pa-md-8
                v-row.mb-2.d-flex.d-md-none(align="center" justify="end")
                  v-btn.white--text(tile small :outlined="openRegisterModal" color="teal darken-1") Sign In
                  v-btn.white--text(tile small :outlined="!openRegisterModal" color="teal darken-1" @click="openRegisterModal = !openRegisterModal") Register
                v-row
                  v-img(height="auto" :src="banner")



            v-col.d-flex.align-start.align-md-end(cols="12" md="5")
                v-container.pt-0.px-5.pb-md-8.px-md-5
                  v-row.mb-2.d-none.d-md-flex(align="center" justify="end")
                    v-btn.white--text(tile small :outlined="openRegisterModal" color="teal darken-1") Sign In
                    v-btn.white--text(tile small :outlined="!openRegisterModal" color="teal darken-1" @click="openRegisterModal = !openRegisterModal") Register

                  v-dialog(width="500" v-model="openRegisterModal")

                    v-card(width="500")
                      v-container
                        v-row( no-gutters)
                          h2.px-5.pt-5.headline Register
                        v-row(no-gutters)
                          v-container
                            RegisterForm

                  v-row(align="center" justify="space-around")
                    v-container
                      v-row
                        v-container.py-0.py-md-3
                          h2.headline.teal--text.darken-1 Sign in with
                      v-row
                        v-container.pb-0.pt-3.py-md-3
                          <!-- for smaller device -->
                          v-btn.mr-2.d-inline.d-md-none(tile small) Google
                          v-btn.mr-2.white--text.d-inline.d-md-none(tile small color="blue darken-3") Facebook
                          <!-- for larger device -->
                          v-btn.mr-2.d-none.d-md-inline(tile large) Google
                          v-btn.mr-2.white--text.d-none.d-md-inline(tile large color="blue darken-3") Facebook

                  v-row( align="end" justify="center")
                    v-container
                      LoginForm


</template>

<script>
import RegisterForm from '../components/RegisterForm'
import Login from '../components/Login'

export default {
  components: {
    RegisterForm,
    LoginForm: Login
  },
  data() {
    return {
      banner: require('../assets/img/reveneu.svg'),
      tab: null,
      openRegisterModal: false
    }
  },
  created() {
    if (this.$auth.isAuthenticated()) {
      this.$router.push({ name: 'donate' })
    }
  }
}
</script>

<style scoped></style>
