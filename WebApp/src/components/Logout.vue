<template>
  <div class="log">
  </div>
</template>

<script>
  export default {
    created () {
      this.$store.dispatch('logoutUser')
    }
  }
</script>

<style scoped>
</style>
