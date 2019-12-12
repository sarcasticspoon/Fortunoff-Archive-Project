<template>
    <div>
        <!-- <Header :app-title="title" /> -->
        <b-navbar variant = "light" text = "light">
          <b-navbar-brand style="color:#1099ab;" > Where Once They Walked : Fortunoff Video Archive Testimony Mapper </b-navbar-brand>
          <!-- <b-nav-form inline class="ml-auto">
              <b-form-input v-model="query.placename" placeholder = "Place"> </b-form-input>
              <b-form-input v-model="query.firstname" placeholder = "FirstName"> </b-form-input> 
              <b-form-input v-model="query.lastname" placeholder = "FirstName"> </b-form-input> 
              <b-button variant = "outline-dark" @click="testy"> Search </b-button>
          </b-nav-form>  -->
        </b-navbar>
        <MappyBoy style="padding-left:30px; padding-right:30px;"/>
        <!-- <p> This exists </p> -->
    </div>
</template>

<script>
import Header from './components/Header.vue';
import MappyBoy from './components/WebMap.vue';

export default {
    name: 'App',
    components: { MappyBoy},
    methods : {
        testy: function () {
            this.show = "peanuts";
        }
    },
    data: () => ({
        query : {
            placename: '',
            firstname: '',
            lastname: ''
        },
        show : "false"
    })
};
</script>

<style lang="scss" scoped>
div {
    font-family: "Georgia", Times, serif;
    display: flex;
    flex-direction: column;
    padding: 0;
    margin: 0;
    width: 100%;
    height: 100%;
}
</style>
