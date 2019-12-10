<template>
    
    <div id="app">
        <!-- <p> This is a thing </p> -->
        <b-navbar variant = "light" text = "light">
          <b-navbar-brand> Fortunoff Archive Project </b-navbar-brand>
          <b-nav-form class="ml-auto">
              <b-form-input placeholder = "Place"> </b-form-input>
              <b-form-input placeholder = "FirstName"> </b-form-input> 
              <b-form-input placeholder = "LastName"> </b-form-input> 
              <b-button variant = "outline-dark"> Search </b-button>
          </b-nav-form>
        </b-navbar>
        <WebMap/>
    </div>
</template>

<script>
import WebMap from './components/WebMap.vue';

export default {
    name: 'App',
    components: { WebMap }
};
</script>

<style>
html,body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
}
#app {
  display: flex;
  flex-direction: column;
  padding: 0;
  margin: 0;
  width: 100%;
  height: 100%;
}
</style>
