<template lang="pug">
  v-form
    v-text-field(
      :rules="[required('email'), emailFormat()]"
      color="teal darken-1"
      label="E-mail")

    v-text-field(:type="isVisible ? 'text' : 'password'"
      :append-icon="isVisible ? 'mdi-eye' : 'mdi-eye-off'"
      :rules="[required('password'), minLength('Password', 8)]"
      @click:append="isVisible = !isVisible"
      color="teal darken-1"
      label="Password")
      

    v-checkbox( color="teal darken-1" label="Remember me")

    <nuxt-link to="/dashboard">
      v-btn.mt-4.white--text( block tile color="teal darken-1") Sign In
    </nuxt-link>
</template>

<script>
import validations from '../utilities/validations'
export default {
  name: 'RegisterForm',
  data() {
    return {
      ...validations,
      isVisible: false
    }
  }
}
</script>

<style scoped></style>
