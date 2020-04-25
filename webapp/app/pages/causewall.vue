<template lang="pug">
  v-layout(column justify-center align-center)
    v-container
      v-row(justify="space-between" align="center")
        v-col(cols="6" md="3")
          h2.primary--text Cause Wall
        v-col(cols="6" md="3" justify="end")
          v-container
            v-row(justify="end")
              v-btn(color="primary" @click="openPostCauseDialog = !openPostCauseDialog") Post a cause
            v-dialog(v-model="openPostCauseDialog" width="500")
              v-card(width="500")
                v-card-title.font-weight-regular Let us know what you need
                v-card-text
                  v-textarea(auto-grow autofocus clearable color="primary" rows="3")
                v-card-actions
                  v-row.px-3(no-gutters justify="space-between" align="center")
                    v-col(cols="12" md="6")
                      v-file-input(color="primary" accept="image/png, image/jpeg, image/bmp" placeholder="Choose a photo" prepend-icon-inner="mdi-camera")
                    v-col.d-flex.justify-end(cols="12" md="6")
                      v-btn(color="primary" @click="openPostCauseDialog = !openPostCauseDialog") Share

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
                v-img(:src="cause.images[0]" min-height="250" width="450" aspect-ratio="8/5")


              v-row.pt-3(no-gutters)
                v-col(cols="6")
                  v-tooltip(bottom)
                    template(v-slot:activator="{on}")
                      v-btn(text large block @click="cause.votes++")
                        v-icon(color="green darken-2" large center) mdi-chevron-up
                        span Up vote ({{ cause.cause_total_up_votes }})
                v-col(cols="6")
                  v-tooltip(bottom)
                    template(v-slot:activator="{on}")
                      v-btn(text large block @click="cause.votes--")
                        v-icon(color="red darken-2" large center) mdi-chevron-down
                        span Down vote ({{ cause.cause_total_down_votes }})


</template>

<script>
export default {
  layout: 'dashboardLayout',
  data() {
    return {
      openPostCauseDialog: false,
      causes: []
    }
  },
  async created() {
    this.causes = await this.$api.listCauses()
  }
}
</script>
