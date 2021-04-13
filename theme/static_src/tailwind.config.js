// This is a minimal config.
// If you need the full config, get it from here:
// https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
module.exports = {
    purge: [
        // Templates within theme app (e.g. base.html)
        '../templates/**/*.html',
        // Templates in other apps. Uncomment the following line if it matches
        // your project structure or change it to match.
        '../../templates/**/*.html',
    ],
    darkMode: false, // or 'media' or 'class'
    theme: {
        extend: {
            colors: {
                'myrtle-green': '#317773',
                'myrtle-green-light': '#51b8b3',
                'languid-lavender': '#e2d1f9',
                'languid-lavender-dark': '#d2b7f6',
                'old-lavender': '#735D78',
                'light-yellow': '#F8FCDA',
            },
            width: {
                '1/10': '10%',
                '2/10': '20',
                '3/10': '20%',
                '4/10': '40%',
                '5/10': '50%',
                '6/10': '60%',
                '7/10': '70%',
                '8/10': '80%',
                '9/10': '90%',
                '10/10': '100%',
            },
        },
    },
    variants: {
        extend: {},
    },
    plugins: [
        require('@tailwindcss/forms'),
        // ...
    ],
}
