<template lang="pug">
  v-layout(column justify-center align-center)
    v-container
      v-row(justify="space-between" align="center")
        v-col(cols="6" md="3")
          h2.primary--text Cause Wall
        v-col(cols="6" md="3" justify="end")
          v-container
            v-row(justify="end")
              v-btn(color="primary" @click="openModal") Post a cause
            //- if user is authenticated, will let him post cause
            v-dialog(v-model="openPostCauseDialog" width="500")
              v-card(width="500")
                v-card-title.font-weight-regular Let us know what you need
                v-card-text
                  v-textarea(v-model="newCauseContent" auto-grow autofocus clearable color="primary" rows="3")
                v-card-actions
                  v-row.px-3(no-gutters justify="space-between" align="center")
                    v-col(cols="12" md="6")
                      v-file-input(v-model="newCauseImage" color="primary" accept="image/png, image/jpeg, image/bmp" placeholder="Choose a photo" prepend-icon-inner="mdi-camera")
                    v-col.d-flex.justify-end(cols="12" md="6")
                      v-btn(color="primary" @click="createNewCause") Post
            //- if user is authenticated, will not let him post cause but register
            v-dialog(width="550" v-model="openJoinDialog")
              LoginOrRegister
    v-divider
    v-container
      v-row(v-for="cause in causes" :key="cause.cause_id" justify="center")
        v-col(cols="12" md="8")
          v-card
            v-container
              v-row(no-gutters)
                v-col(cols="12")
                  v-card-title.pa-0
                    v-container.pb-0
                      v-row(no-gutters)
                        v-col(cols="6")
                          v-list.py-0
                            v-list-item.px-0
                              v-list-item-avatar
                                v-icon(x-large) mdi-account-circle
                                //- v-img(:src="inquire.avatar")
                              v-list-item-content(two-line)
                                v-list-item-title {{ cause.user_name }}
                                v-list-item-subtitle {{ new Date(cause.cause_created_at).toLocaleString('en-US', { dateStyle: 'long', timeStyle: 'medium' }) }}
                        //- v-col.d-flex.align-center.justify-end(cols="6")
                        //-   v-btn(medium raised color="primary") Donate
              v-row(no-gutters)
                v-col(cols="12")
                  v-card-text
                    h2.font-weight-regular {{ cause.content }}
              v-row.px-3(no-gutters)
                v-img(:src="cause.images[0]" min-height="250" width="450" contain)
              v-row.pt-3(no-gutters)
                v-col(cols="6")
                  v-tooltip(bottom)
                    template(v-slot:activator="{on}")
                      v-btn.px-0.px-md-3(text large block @click="giveVote(cause.cause_id, 'UP', cause.SK)")
                        v-icon(color="green darken-2" large center) mdi-chevron-up
                        span Up vote ({{ cause.cause_total_up_votes }})
                v-col(cols="6")
                  v-tooltip(bottom)
                    template(v-slot:activator="{on}")
                      v-btn.px-0.px-md-3(text large block @click="giveVote(cause.cause_id, 'DOWN', cause.SK)")
                        v-icon(color="red darken-2" large center) mdi-chevron-down
                        span Down vote ({{ cause.cause_total_down_votes }})
    v-snackbar(v-model="vote" :color="snackbarColor")
      h2 {{snackbarMessage}}
</template>
<script>
import LoginOrRegister from '../components/loginOrRegister'
export default {
  components: {
    LoginOrRegister
  },
  layout: 'dashboardLayout',
  data() {
    return {
      openRegisterModal: false,
      isAuthenticated: false,
      openPostCauseDialog: false,
      newCauseContent: '',
      newCauseImage: null,
      causes: [],
      snackbarMessage: 'Voted!',
      snackbarColor: 'green darken-2',
      vote: false
    }
  },
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
  async created() {
    this.causes = await this.$api.listCauses()
    if (this.$auth.isAuthenticated()) {
      this.isAuthenticated = true
    }
  },
  updated() {
    console.log(this.causes)
  },
  methods: {
    openModal() {
      if (this.isAuthenticated) {
        this.openPostCauseDialog = true
      } else {
        this.$store.commit('auth/setJoinDialog', true)
      }
    },
    async createNewCause() {
      const userId = this.$auth.getUser().sub
      const image = await this.$api.uploadCauseImage({
        userId,
        image: this.newCauseImage
      })
      await this.$api.createCause({
        userId,
        content: this.newCauseContent,
        imageUrl: image.image_url
      })
      this.causes = await this.$api.listCauses()
      this.openPostCauseDialog = false
    },
    async giveVote(causeId, voteType, SK) {
      if (this.isAuthenticated) {
        const data = {
          userId: this.$auth.getUser().sub,
          causeId,
          voteType,
          SK
        }
        try {
          const res = await this.$api.giveVote(data)
          this.snackbarColor = 'green darken-2'
          this.snackbarMessage = 'Voted!'
          this.vote = true
          this.causes = await this.$api.listCauses()
          console.log(res)
        } catch (err) {
          this.snackbarColor = 'red darken-2'
          this.snackbarMessage = 'Already voted!'
          this.vote = true
        }
      } else {
        this.$store.commit('auth/setJoinDialog', true)
      }
    }
  }
}
</script>
