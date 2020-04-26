import Vue from 'vue'
import Amplify, * as AmplifyModules from '@aws-amplify/core'
import { AmplifyPlugin } from 'aws-amplify-vue'

Amplify.configure({
  Auth: {
    region: process.env.AWS_REGION,
    userPoolId: process.env.COGNITO_USER_POOL_ID,
    userPoolWebClientId: process.env.COGNITO_CLIENT_ID,
    oauth: {
      domain: process.env.COGNITO_DOMAIN,
      scope: [
        'email',
        'openid',
        'phone',
        'profile',
        'aws.cognito.signin.user.admin'
      ],
      redirectSignIn: window.location.origin,
      redirectSignOut: window.location.origin,
      responseType: 'token' // or 'token', note that REFRESH token will only be generated when the responseType is code
    }
  }
})

Vue.use(AmplifyPlugin, AmplifyModules)
export default (_, inject) => {
  inject('Amplify', AmplifyModules)
}
