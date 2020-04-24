<template lang="pug">
  v-app
    v-app-bar(fixed color="teal darken-1")
      v-container
        v-toolbar-title.ml-0.ml-md-12.pl-0.pl-md-7.font-weight-medium.white--text(:class="{'headline': $vuetify.breakpoint.mdAndDown, 'display-1': $vuetify.breakpoint.mdAndUp}"  v-text="title")
           
    v-content
      v-container
        nuxt
</template>
<script>
export default {
  data() {
    return {
      title: 'Momentous'
    }
  }
}
</script>
