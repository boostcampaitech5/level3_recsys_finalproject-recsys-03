const { createProxyMiddleware } = require('http-proxy-middleware');

const backendUrl = process.env.REACT_APP_BACKEND_HOST;

module.exports = function (app) {
  app.use(
    '/api/recommendMusic',
    createProxyMiddleware({
      target: backendUrl,
      pathRewrite: {
        '^/api': '',
      },
    })
  );
};
