import AmplifyAuth from '@aws-amplify/auth'
import Auth from '@/utils/auth'

export default async ({ store, route }, inject) => {
  const auth = new Auth({
    amplifyAuth: AmplifyAuth,
    store
  })
  inject('auth', auth)

  try {
    // handle cognito social user linking bug
    if (
      route.hash.startsWith(
        '#error_description=Already+found+an+entry+for+username+'
      )
    ) {
      await auth.federatedLogin({
        provider: route.hash
          .split('#error_description=Already+found+an+entry+for+username+')[1]
          .split('_')[0]
      })
    }
    // fetch existing session
    await auth.fetchSession()
  } catch (err) {}
}
