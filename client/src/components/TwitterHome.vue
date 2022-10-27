<template>
  <div class="container">
    <h1 class="mt-5">{{ msg }}</h1>
    <div class="card p-3 col-sm-12">
      <div class="card-body">
        <form v-on:submit.prevent="submitForm">
          <div class="input-group mb-3">
            <span class="input-group-text">Name</span>
            <input type="text" class="form-control" id="name" v-model="name" required>
          </div>
          <div class="input-group mb-3">
            <span class="input-group-text">Tweet</span>
            <textarea class="form-control" id="description" v-model="description" @input="assertMaxChars()"
              required></textarea>
          </div>
          <p class="text-danger" v-if="bReachedMaxLength">Max Length is 50</p>
          <div class="mt-3">
            <button type="submit" class="btn btn-success">Add Tweet</button>
          </div>
        </form>
      </div>
    </div>

    <table class="table table-dark table-striped mt-5">
      <thead>
        <tr>
          <th class="sortable" @click="sort('name')">Name</th>
          <th>Tweet</th>
          <th class="sortable" @click="sort('created_at')">Created</th>
        </tr>
      </thead>
      <tbody v-if="sortedTweets.length > 0">
        <tr v-for="tweet in sortedTweets" :key="tweet.id">
          <td>{{ tweet.name }}</td>
          <td>{{ tweet.description }}</td>
          <td>{{ new Date(tweet.created_at).toLocaleDateString() }} {{ new Date(tweet.created_at).toLocaleTimeString()
          }}</td>
        </tr>
      </tbody>
    </table>

  </div>
</template>

<script>

import axios from 'axios'
import { isProxy, toRaw } from 'vue'

export default {
  name: 'TwitterHome',
  props: {
    msg: String
  },
  data() {
    return {
      tweets: [''],
      title: '',
      description: '',
      descriptionMaxLengthInCars: 50,
      sortDirection: 1,
      sortBy: 'created_at',
      bReachedMaxLength: false
    }
  },
  methods: {
    sort(type) {
      this.sortBy = type
      this.sortDirection *= -1
    },
    assertMaxChars: function () {
      this.bReachedMaxLength = this.description.length > this.descriptionMaxLengthInCars
      if (this.description.length >= this.descriptionMaxLengthInCars) {
        this.description = this.description.substring(0, this.descriptionMaxLengthInCars)
      }
    },
    getData() {
      axios.get('http://localhost:8000/api/tweets/').then((response) => {
        this.tweets = response.data
      }).catch((error) => {
        console.log(error)
      })
    },
    submitForm() {
      axios.post('http://localhost:8000/api/tweets/', {
        name: this.name,
        description: this.description
      }).then((response) => {
        this.tweets.push(response.data)
        this.name = ''
        this.description = ''
      }).catch((error) => {
        console.log(error)
      })
    },
    sortMethods(type, head, direction) {
      switch (type) {
        case 'String': {
          return direction === 1 ?
            (a, b) => a[head].localeCompare(b[head]) :
            (a, b) => b[head].localeCompare(a[head])
        }
        case 'Date': {
          return direction === 1 ?
            (a, b) => new Date(b[head]) - new Date(a[head]) :
            (a, b) => new Date(a[head]) - new Date(b[head])
        }
        case 'Number': {
          return direction === 1 ?
            (a, b) => Number(b[head]) - Number(a[head]) :
            (a, b) => Number(a[head]) - Number(b[head])
        }
      }
    }
  },
  created() {
    this.getData()
  },
  computed: {
    sortedTweets() {
      const type = this.sortBy === 'name' ? 'String' : 'Date'
      const direction = this.sortDirection
      const head = this.sortBy
      if (this.tweets.length == 0) {
        return this.tweets
      }
      // eslint-disable-next-line vue/no-side-effects-in-computed-properties
      let sorted = this.tweets.sort(this.sortMethods(type, head, direction))
      if (sorted.length == 1 && sorted[0] === '') {
        return []
      }
      return isProxy(sorted) ? toRaw(sorted) : sorted
    }
  }
}
</script>
<style scoped>
th.sortable {
  cursor: pointer
}
</style>
