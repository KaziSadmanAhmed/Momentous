<template lang="pug">
  v-layout.mt-12( column justify-center align-center)
    v-container.justify-start.mt-md-12
      v-card.mx-auto.my-12(max-width="400")
        v-container
          v-row(justify="center")
            v-col(cols="12" xs="4" lg="6")
              v-container.pa-md-8
                v-row.mb-6(align="center")
                  span {{ hashesPerSecond }} hashes/s
                v-row(align="center")
                  span {{threads}} threads + / -
            v-col(cols="12" xs="4" lg="6")
              v-container.pa-md-8
                v-row.mb-6(align="center")
                  span {{ totalHashes }} total hashes
                v-row(align="center")
                  span {{ speed }} % speed + / -

          v-row(justify="center")
            v-btn(@click="toggleMining" :disabled="!miner")
              v-icon.mr-2 mdi-play
              v-spacer
              span(v-if="miner && miner.isRunning()") Stop donating
              span(v-else) Start donating
</template>
<script>
export default {
  head() {
    return {
      script: [
        {
          src: process.env.COINIMP_CLIENT_URL,
          defer: true,
          callback: () => this.createMiner()
        }
      ]
    }
  },
  data() {
    return {
      miner: null
    }
  },
  computed: {
    hashesPerSecond() {
      return this.miner ? this.miner.getHashesPerSecond().toFixed(2) : 0
    },
    totalHashes() {
      return this.miner ? this.miner.getTotalHashes() : 0
    },
    threads: {
      get() {
        return this.miner ? this.miner.getNumThreads() : 0
      },
      set(number) {
        if (this.miner) {
          this.miner.getNumThreads(number)
        }
      }
    },
    speed: {
      get() {
        return this.miner ? (1 - this.miner.getThrottle()) * 100 : 0
      },
      set(number) {
        if (this.miner) {
          const throttle = 1 - number / 100
          this.miner.setThrottle(throttle)
        }
      }
    }
  },
  methods: {
    createMiner() {
      this.miner = new window.Client.Anonymous(process.env.COINIMP_SITE_KEY, {
        throttle: 0,
        c: 'w',
        ads: 0
      })
    },
    toggleMining() {
      this.miner &&
        (this.miner.isRunning() ? this.miner.stop() : this.miner.start())
    }
  }
}
</script>
