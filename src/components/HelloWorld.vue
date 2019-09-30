<template>
<div class="">

  <section class="hero is-fullheight is-light is-info">
    <div class="hero-head ">
      <nav class="navbar is-dark">
        <div class="navbar-brand">
          <a class="navbar-item" href="">
            <span class="title is-5">Preasy</span>
          </a>
          <div class="navbar-burger" @click="showNav = !showNav" :class="{ 'is-active': showNav }">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>

        <div class="navbar-menu" :class="{ 'is-active': showNav }">
          <div class="navbar-end">
            <a class="navbar-item has-text-light" v-on:click="setMyPrintTray()">
              <p>Print Tray</p>
            </a>
            <a class="navbar-item has-text-light" v-on:click="setMyPickUp()">
              <p>Pick Ups ( {{ getPickUpNumber() }} )</p>
            </a>
          </div>
        </div>
      </nav>

    </div>

    <div class="container has-text-centered">
      <div class="card" v-for="file in getReleventFiles()">
        <div class="card-content">
          <!-- v-if="file.printJobStatus === 0"> -->
          <div class="content">
            <div class="level is-mobile">
              <div class="level-left">
                <div class="level-item">
                  <!-- <span>{{ file.docfile }}</span> -->
                  <span>{{ getFileName(file.docfile) }}</span>
                </div>
              </div>
              <div class="level-right">
                <div class="level-item">
                  <span>Pages</span>
                </div>
                <div class="level-item">
                  <span>Price</span>
                </div>
                <div class="level-item">
                  <!-- <a class="delete is-danger" v-on:click="removeFile(file.id)"></a> -->
                  <a class="button is-danger" v-on:click="removeFile(file.id)">{{ getFileStatus(file.printJobStatus) }}</a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="container has-text-centered">
        <div class="tile" v-if="getReleventFiles().length === 0">
          <p class="title is-4">No files in print tray.</p>
          <p class="subtitle">Check Pick Up Queue</p>
        </div>
      </div>

    </div>
    <!-- </div> -->
    <div class="hero-footer">
      <div class="container">
        <input type="file" ref="file" style="display: none" v-on:change="addFile()" />
        <a @click="$refs.file.click()" class="button is-danger is-rounded" v-if="active_tab === 'my_print_tray'">Add File</a>

        <br>
        <br>

        <a class="button is-dark is-fullwidth is-large" v-on:click="actionButton()">
          <span>{{ this.action_button_text }}</span>
        </a>
        <br>
        <br>
      </div>
    </div>

  </section>


</div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'HelloWorld',
  data() {
    return {
      files: [], // Array for holding the files.
      api_host: 'http://192.168.1.103:8000',
      // api_host: 'localhost:8000',
      // api_host: '127.0.0.1:8000',
      showNav: true,
      action_button_text: "Print Files",
      active_tab: "my_print_tray",

    }
  },

  computed: {

  },

  mounted() {
    this.getFiles();
  },
  methods: {
    getFiles() {
      axios({
        method: 'get',
        url: this.api_host + '/file2/files/',
      }).then(response => this.files = response.data);
    },

    removeFile(file_id) {
      axios({
        method: 'delete',
        url: this.api_host + '/file2/files/' + file_id,
      }).then(response => this.getFiles());
    },

    addFile() {

      let docfile = this.$refs.file.files[0];
      let formData = new FormData();
      formData.append('docfile', docfile);

      axios({
        method: 'post',
        url: this.api_host + '/file2/files/upload/',
        data: formData,
        config: {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }

      }).then(response => this.getFiles());
    },

    getFileName(docfile) {
      return docfile.split('/').pop().substring(0, 15)
    },

    actionButton() {

      if (this.active_tab === 'my_print_tray') {
        console.log('send print tray')

        let printTray = this.files.filter(function(file) {
          return file.printJobStatus == 0;
        })

        let printTrayIds = printTray.map(a => a.id);

        axios({
          method: 'put',
          url: this.api_host + '/file2/files/printmytray',
          data: printTrayIds
        }).then(response => this.getFiles());

      } else if (this.active_tab === 'my_pick_up') {
        console.log('im here to pick up');
        let pickUp = this.files.filter(function(file) {
          return file.printJobStatus == 2;
        })

        let pickUpIds = pickUp.map(a => a.id);

        axios({
          method: 'put',
          url: this.api_host + '/file2/files/pickup',
          data: pickUpIds
        }).then(response => this.getFiles());

      }
    },

    setMyPrintTray() {
      this.active_tab = "my_print_tray";
      this.action_button_text = "Print Files"
    },

    setMyPickUp() {
      this.active_tab = "my_pick_up";
      this.action_button_text = "Pick-Up"
    },

    getReleventFiles() {
      if (this.active_tab === 'my_print_tray') {
        return this.files.filter(function(file) {
          return file.printJobStatus == 0;
        });
      } else if (this.active_tab === 'my_pick_up') {
        return this.files.filter(function(file) {
          return file.printJobStatus == 1;
        });
      }
    },

    getFileStatus(file_status) {
      console.log(file_status);
      switch (file_status) {
        case 0:
          return 'Remove'
          break;

        case 1:
          return 'In Queue'
          break;

        case 2:
          return 'Printed'
          break;

        case 3:
          return 'Picked'
          break;

        default:
          return 'Lost in Ether'
      }
    },

    getPickUpNumber() {
      return this.files.filter(function(file) {
        return file.printJobStatus == 1;
      }).length;
    },

  }
}
</script>


<style>
.level-is-shrinkable {
  flex-shrink: 1;
}
</style>
