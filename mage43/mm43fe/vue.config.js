const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  // Vue配置，实际作用在webpack的devServer上
  // devServer: {
  //   proxy: {
  //     '/api/v1': {
  //       target: 'http://127.0.0.1:5000', // 后端配置，rewrite路径重写，后续使用nginx代替
  //       pathRewrite: { '^/api/v1': '' },
  //     }
  //   }
  // },
  // 配置WebPack
  // configureWebpack: config => {
  //   if (process.env.NODE_ENV === 'production') {
  //     // 为生产环境修改配置...
  //   } else {
  //     // 为开发环境修改配置...
  //     config.devServer = {
  //       proxy: {
  //         '/api/v1': {
  //           target: 'http://127.0.0.1:5000', // 后端配置，rewrite路径重写，后续使用nginx代替
  //           pathRewrite: { '^/api/v1': '' },
  //         }
  //       }
  //     }
  //   }
  // },
  // 配置WebPack 链式
  chainWebpack: config => {
    config
    .when(process.env.NODE_ENV === 'production',  
      config => {
        // 为生产环境修改配置...
        config.plugin('html').tap(args => {
          args[0].title = 'FlyOps运维平台'
          return args
        })
      },
      config => {
        // 为开发环境修改配置...
        config.devServer.proxy({
          '/api/v1': {
            target: 'http://127.0.0.1:5000', // 后端配置，rewrite路径重写，后续使用nginx代替
            pathRewrite: { '^/api/v1': '' },
          }
        }),
        config.plugin('html').tap(args => {
          console.log(args, '~~~~')
          args[0].title = 'FlyOps运维平台-Dev'  // 修改title
          return args
        })
      }
    )
  }
})
