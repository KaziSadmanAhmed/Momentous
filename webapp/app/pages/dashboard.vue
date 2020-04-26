<template lang="pug">
  v-layout(column justify-center align-center)
    v-container
      v-row( align="center" justify="space-between")
        v-col(cols="6" md="3")
          h2.teal--text.darken-1 Dashboard
        v-col(cols="6" md="3" justify="end")
          v-container
            v-row(justify="end")
              v-btn(tile
                small
                dark
                color="teal darken-1"
                class="d-block d-md-none") Support
              v-btn(tile
                large
                dark
                color="teal darken-1"
                class="d-none d-md-block") Contact Support

    v-container
      v-row
        v-col(cols="12" md="8")
          v-container(class="pt-3 pt-md-0")
            v-row
              v-col(cols="12" md="6" class="px-0 pr-md-3 pl-md-0 pt-md-0")
                v-card(max-height="500")
                  v-toolbar( color="teal darken-1" dark dense)
                    v-toolbar-title Daily Goals

                  v-card-text
                    div Word of the Day
                    p.display-1.text--primary be•nev•o•lent
                    p adjective
                    div.text--primary well meaning and kindly.<br /> "a benevolent smile"

                  <v-card-content></v-card-content>
              v-col(cols="12" md="6" class="px-0 pl-md-3 pt-md-0")
                v-card(max-height="500")
                  v-toolbar(color="teal darken-1" dark dense)
                    v-toolbar-title Weekly Goals

                  v-card-text
                    div Word of the Day
                    p.display-1.text--primary be•nev•o•lent
                    p adjective
                    div.text--primary well meaning and kindly.<br /> "a benevolent smile"
                      
            v-row
              v-col(cols="12" class="pa-0 pl-md-0")
                v-card(max-height="500")
                  v-toolbar( color="teal darken-1" dark dense)
                    v-toolbar-title Overall Progress

                  v-card-text
                    div Word of the Day
                    p.display-1.text--primary be•nev•o•lent
                    p adjective
                    div.text--primary well meaning and kindly.<br /> "a benevolent smile"
                    
        v-col(cols="12" md="4")
          v-card.mx-auto( max-width="500")
            v-toolbar( color="teal darken-1" dark dense)
              v-toolbar-title Leaderboard
            v-list
              v-list-item(v-for="item in items" :key="item.id")
                v-list-item-avatar(tile)
                  v-img(:src="item.avatar")

                v-list-item-content(two-line)
                  v-list-item-title( v-text="item.title")
                  v-list-item-subtitle {{ item.profession }}

                v-list-item-icon
                  v-icon(v-if="item.icon" color="pink") mdi-star
</template>
<script>
export default {
  layout: 'dashboardLayout',
  data() {
    return {
      items: [
        {
          id: 1,
          icon: true,
          title: 'Jason Oner',
          avatar: 'https://cdn.vuetifyjs.com/images/lists/1.jpg',
          profession: 'Engineer'
        },
        {
          id: 2,
          title: 'Travis Howard',
          avatar: 'https://cdn.vuetifyjs.com/images/lists/2.jpg',
          profession: 'Doctor'
        },
        {
          id: 3,
          title: 'Ali Connors',
          avatar: 'https://cdn.vuetifyjs.com/images/lists/3.jpg',
          profession: 'Health professional'
        },
        {
          id: 4,
          title: 'Cindy Baker',
          avatar: 'https://cdn.vuetifyjs.com/images/lists/4.jpg',
          profession: 'Social Activist'
        },
        {
          id: 5,
          icon: true,
          title: 'Jason Oner',
          avatar: 'https://cdn.vuetifyjs.com/images/lists/1.jpg',
          profession: 'Engineer'
        },
        {
          id: 6,
          title: 'Travis Howard',
          avatar: 'https://cdn.vuetifyjs.com/images/lists/2.jpg',
          profession: 'Doctor'
        },
        {
          id: 7,
          title: 'Ali Connors',
          avatar: 'https://cdn.vuetifyjs.com/images/lists/3.jpg',
          profession: 'Health professional'
        }
      ]
    }
  }
}
</script>
