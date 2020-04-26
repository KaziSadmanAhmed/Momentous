<template lang="pug">
  v-layout(column justify-center align-center)
    v-container
      v-row(justify="space-between" align="center")
        v-col(cols="6" md="3")
          h2.teal--text.darken-1 Leaderboard
        v-col(cols="6" md="3" justify="end")
          v-container
            v-row(justify="end")
              //- v-btn.d-block.d-md-none(color="primary") support
      v-divider
      v-row.mt-10(no-gutters justify="center")
        v-col(cols="12" md="8")
          v-card
            v-toolbar(color="primary" dark dense)
              v-toolbar-title Leaderboard
            v-list.overflow-y-auto(max-height="600")
              v-list-item(v-for="(user, index) in leaderboard" :key="user.user_id" @click)
                v-list-item-icon
                  v-btn(fab small color="primary" v-text="index + 1")
                v-list-item-avatar
                  //- v-img(:src="item.avatar")
                  v-icon(x-large) mdi-account-circle
                v-list-item-content.pl-5(two-line)
                  v-list-item-title(v-text="user.user_name")
                v-list-item-action
                  v-list-item-action-text
                    span.headline(v-text="user.hash_generated_total")
                    span.body-1  hashes
                  //- v-list-item-subtitle {{ item.profession}}
                //- v-spacer
                //- v-spacer
                //- v-spacer
                //- v-list-item-content
                //-   v-list-item-title.title {{index + 1}}
                //- v-list-item-icon
                //-   v-btn.elevation-2(fab small :color="item.up ? 'green' : item.down ? 'red' : 'orange'" dark)
                //-     v-icon {{item.up ? 'mdi-arrow-up-bold' : item.down ? 'mdi-arrow-down-bold' : 'mdi-arrow-left-right-bold'}}

</template>

<script>
export default {
  layout: 'dashboardLayout',
  data() {
    return {
      leaderboard: []
    }
  },
  async created() {
    this.leaderboard = await this.$api.getLeaderboard()
  }
}
</script>
