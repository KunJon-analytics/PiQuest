var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');


const main = (name, minimize) => ({
    entry: './assets/js/index',
    mode: "production",
    optimization: {
        minimize,
        usedExports: true
    },
    resolve: {
        extensions: ['.js'],
    },
    output: {
        globalObject: "this",
        filename: name,
        path: path.resolve('./assets/webpack_bundles/'),
    },
    plugins: [
        new BundleTracker({ filename: './webpack-stats.json' })
    ]
});

module.exports = [
    {
        ...main('[name]-[hash].js', false),
        devtool: 'inline-source-map',
        mode: "development",
    },
    {
        ...main('[name]-[hash].min.js', true)
    }
];