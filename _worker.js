export default {
  async fetch(request, env, ctx) {
    // `env.ASSETS`
    return env.ASSETS.fetch(request);
  }
};