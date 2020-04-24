<template lang="pug">
  v-layout.mt-12( column justify-center align-center)
    v-container.justify-start.mt-md-12
      v-card.mx-auto.my-12(max-width="400")
        v-container
          v-row(justify="center")
            v-col(cols="12" xs="4" lg="6")
              v-container.pa-md-8
                v-row.mb-6(align="center")
                  span {{hashes}} hashes/s
                v-row(align="center")
                  span {{threads}} threads + / -
            v-col(cols="12" xs="4" lg="6")
              v-container.pa-md-8
                v-row.mb-6(align="center")
                  span {{total}} total
                v-row(align="center")
                  span {{speedPercentage}} % speed + / -

          v-row(justify="center")
            v-btn 
              v-icon.mr-2 mdi-play
              v-spacer
              span Start Mining
</template>
<script>
export default {
  data() {
    return {
      hashes: 0,
      threads: 4,
      total: 14,
      speedPercentage: 100
    }
  }
}
</script>
