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
            <a class="navbar-item has-text-light" v-bind:class="{ 'is-active': isActiveMyPrintTray }" v-on:click="setMyPrintTray()">
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
                  <a class="button" :class="[ actionButtonColor()? 'is-danger' : 'is-light' ]" v-on:click="removeFile(file.id)">{{ getFileStatus(file.printJobStatus) }}</a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="container has-text-centered">
        <div class="tile" v-if="getReleventFiles().length === 0">
          <p class="title is-4">No files in print tray.</p>
          <p class="subtitle ">{{ getPickUpNumber() }} Files in Pick Up Queue</p>
        </div>
      </div>

    </div>
    <!-- </div> -->
    <div class="hero-footer">
      <div class="container">
        <input id="fileupload" type="file" ref="file" style="display: none" v-on:change="addFile()" />
        <a @click="$refs.file.click()" class="button is-danger is-rounded" v-if="active_tab === 'my_print_tray'">Add File</a>

        <br>
        <br>

        <a class="button is-warning is-rounded is-large" v-on:click="actionButton()">
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
      // api_host: 'http://192.168.43.199:8000',
      api_host: 'http://192.168.1.102:8000',
      // api_host: 'http://192.168.0.103:8000',
      // api_host: 'localhost:8000',
      // api_host: 'http://127.0.0.1:8000',
      showNav: true,
      action_button_text: "Print Files",
      active_tab: "my_print_tray",

    }
  },

  computed: {
    isActiveMyPrintTray: function() {
      return this.active_tab === 'my_print_tray';
    },

    isActiveMyPickUp: function() {
      return this.active_tab === 'my_pick_up';
    }
  },

  mounted() {
    this.getFiles();
  },
  methods: {
    getFiles() {

      axios({
        method: 'get',
        headers: {
          'Authorization': "bearer " + this.$store.state.accessToken
        },
        url: this.api_host + '/file2/files/',
      }).then(response => this.files = response.data);
    },

    removeFile(file_id) {

      if (this.active_tab === 'my_print_tray') {

        axios({
          method: 'delete',
          headers: {
            'Authorization': "bearer " + this.$store.state.accessToken
          },
          url: this.api_host + '/file2/files/' + file_id,
        }).then(response => this.getFiles());

      }
    },

    checkFile(file) {

      var sFileName = file.name;
      var sFileExtension = sFileName.split('.')[sFileName.split('.').length - 1].toLowerCase();
      var iFileSize = file.size;
      var iConvert = (file.size / 1048576).toFixed(2);

      var valid_type = ["doc", "docx"]

      console.log('in checkFile');

      if (!(valid_type.includes(sFileExtension) || iFileSize > 10485760)) { /// 10 mb
        var txt;
        txt = "File type : " + sFileExtension + "\n\n";
        txt += "Size: " + iConvert + " MB \n\n";
        txt += "Please make sure your file is in docx or doc format and less than 10 MB.\n\n";
        alert(txt);
        console.log('File not supported');
        return false;
      }
      console.log('File supported');
      return true;

    },

    addFile() {
      console.log('in addFile');
      console.log(this.$refs.file.files);
      let docfile = this.$refs.file.files[0];

      if (this.checkFile(docfile)) {
        let formData = new FormData();
        formData.append('docfile', docfile);

        axios({
          method: 'post',
          headers: {
            'Authorization': "bearer " + this.$store.state.accessToken
          },
          url: this.api_host + '/file2/files/upload/',
          data: formData,
          config: {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        }).then(response => this.getFiles());

        document.getElementById('fileupload').value = "";
      }
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
          headers: {
            'Authorization': "bearer " + this.$store.state.accessToken
          },
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
          headers: {
            'Authorization': "bearer " + this.$store.state.accessToken
          },
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
      this.getFiles();
      this.active_tab = "my_pick_up";
      this.action_button_text = "Here to Pick-Up"
    },

    getReleventFiles() {
      if (this.active_tab === 'my_print_tray') {
        return this.files.filter(function(file) {
          return file.printJobStatus == 0;
        });
      } else if (this.active_tab === 'my_pick_up') {
        return this.files.filter(function(file) {
          var t_list = [1, 2, 3];
          return t_list.includes(file.printJobStatus);
          // TODO: change filter
        });
      }
    },

    getFileStatus(file_status) {
      // console.log(file_status);
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
          return 'Pick-Up'
          break;

        case 4:
          return 'Picked'
          break;

        default:
          return 'Lost in Ether'
      }
    },

    getPickUpNumber() {
      return this.files.filter(function(file) {
        var t_list = [1, 2, 3];
        return t_list.includes(file.printJobStatus);
      }).length;
    },

    actionButtonColor() {
      if (this.active_tab === 'my_print_tray') {
        return true;
      } else if (this.active_tab === 'my_pick_up') {
        return false;
      }
    },

  }
}
</script>


<style>
.level-is-shrinkable {
  flex-shrink: 1;
}
</style>
