<template>
  <section class="hero is-primary is-fullheight">
    <div class="hero-body">
      <div class="container">
        <div class="columns is-centered">
          <div class="column is-5-tablet is-4-desktop is-3-widescreen">
            <form action="" class="box">
              <div class="field">
                <label for="" class="label">Username</label>
                <div class="control has-icons-left">
                  <input type="text" placeholder="e.g. chinmay" class="input" required v-model="username">
                  <span class="icon is-small is-left">
                    <i class="fa fa-envelope"></i>
                  </span>
                </div>
              </div>
              <div class="field">
                <label for="" class="label">Email</label>
                <div class="control has-icons-left">
                  <input type="email" placeholder="e.g. chinmay@example.com" class="input" required v-model="email">
                  <span class="icon is-small is-left">
                    <i class="fa fa-envelope"></i>
                  </span>
                </div>
              </div>
              <div class="field">
                <label for="" class="label">Password</label>
                <div class="control has-icons-left">
                  <input type="password" placeholder="*******" class="input" required v-model="password">
                  <span class="icon is-small is-left">
                    <i class="fa fa-lock"></i>
                  </span>
                </div>
              </div>
              <div class="field">
                <button class="button is-success" v-on:click="registerUser">
                  Register
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
  export default {
    name: 'Register',
    data () {
      return {
        username: '',
        password: '',
        email: '',
        wrongCred: false // activates appropriate message if set to true
      }
    },
    methods: {
      registerUser () { // call registerUser action
        this.$store.dispatch('registerUser', {
          username: this.username,
          password: this.password,
          email: this.email
        })
          .then(() => {
            this.wrongCred = false
            this.$router.push({ name: 'HelloWorld' })
          })
          .catch(err => {
            console.log(err)
            this.wrongCred = true // if the credentials were wrong set wrongCred to true
          })
        }
      }
  }
</script>

<style scoped>

</style>
