<template>
    <div>
      <form @submit.prevent="submitForm">
        <label for="name">name:</label>
        <input type="text" id="name" v-model="formData.name" autocomplete="name" required>
  
        <label for="age">age:</label>
        <input type="text" id="age" v-model="formData.age" autocomplete="age" required>
  
        <label for="gender">gender:</label>
        <input type="text" id="gender" v-model="formData.gender" autocomplete="gender" required>
  
        <label for="detail">detail:</label>
        <input type="text" id="detail" v-model="formData.detail" autocomplete="detail" required>
  
        <button type="submit">Submit</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        formData: {
          name: '',
          age: '',
          gender: '',
          detail: '',
        },
      };
    },
    methods: {
      submitForm() {
        // 使用 Axios 發送 POST 請求到 Flask 服務器
        axios.post('http://127.0.0.1:5002/add_info', this.formData)
          .then(response => {
            // 在這裡處理服務器的回應
            console.log(response.data);
          })
          .catch(error => {
            // 在這裡處理錯誤
            console.error(error);
          });
      },
    },
  };
  </script>
  
  <style>
  /* 添加樣式，可選 */
  </style>