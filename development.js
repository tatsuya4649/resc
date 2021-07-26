import path from 'path'
import HtmlWebpackPlugin from 'html-webpack-plugin'

const src = path.resolve(__dirname,'./resc/resclog/logserver/static/')
const distjs = path.resolve(__dirname,'./resc/resclog/logserver/static/public/js/')

export default {
	mode: 'development',
        entry: src + "/js/index.js",
        output: {
                path: distjs,
                filename: 'index-bundle.js',
        },
	module: {
		rules: [
		{
			test: /\.js$/,
			exclude: /node_modules/,
			loader: 'babel-loader'
		}
		]
	},
	resolve: {
		extensions: ['.js']
	},
	plugins: [
		new HtmlWebpackPlugin({
			template: src+'/html/index.html',
			filename: 'index.html'
		})
	]
};

