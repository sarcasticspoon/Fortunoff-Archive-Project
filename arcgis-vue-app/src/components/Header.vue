<template>
    <header>
        <span> WAKE UP </span>
    </header>
</template>

<script lang="ts">
export default {
    name: 'Header'
};
</script>

<style lang="scss" scoped>
$blue: #0079c1;
$gray: #959595;
$white: #fff;

header {
    background-color: black;
    color: $white;
    width: 100%;
    height: 2rem;
    line-height: 2rem;
    position: relative;
    font-weight: 400;
    font-style: normal;
    border-bottom: 1px solid $gray;
    text-align: center;
    span {
        vertical-align: middle;
    }
}
</style>
