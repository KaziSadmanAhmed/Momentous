import API from '@/utils/api'

export default function({ $axios, redirect }, inject) {
  // Create a custom axios instance
  const axios = $axios.create({
    baseURL: process.env.API_URL
  })

  const api = new API({
    http: axios
  })

  // Inject to context as $api
  inject('api', api)
}
