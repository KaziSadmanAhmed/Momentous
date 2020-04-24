<template lang="pug">
  v-app
    <!-- navigation drawer of this app -->
    v-navigation-drawer(v-model="drawer" color="teal darken-1" :right="right" :clipped="clipped" fixed app dark)
      v-container
        v-row(align="center" justify="center") 
          v-avatar(size="150")
            v-img(:src="profile")
        v-row.pt-3(align="center" justify="center")
          h3.white--text.text-center Iron Man
        v-row(align="center" justify="center")
          p.white--text.text-center contact@ironman.com
      v-divider
      v-container
        v-list(dense nav class="py-0")
          v-list-item(v-for="item in items" :key="item.title" link)
            v-list-item-content
              v-list-item-title
                h3.text-center {{ item.title }}
      <!-- logout button -->
      template(v-slot:append)
        div.pa-2.mb-5.mb-md-12
          nuxt-link(to="/")
            v-btn( outlined block color="white") Sign out
    <!-- Content of this app   -->
    v-content
      v-container
        nuxt
</template>
<script>
export default {
  data() {
    return {
      drawer: true,
      profile: require('../assets/img/ironMan.jpeg'),
      item: 0,
      items: [
        { title: 'Dashboard' },
        { title: 'Profile' },
        { title: 'Settings' }
      ],
      right: false,
      miniVariant: false,
      clipped: false
    }
  }
}
</script>
