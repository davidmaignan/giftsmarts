module.exports = function(grunt) {

    grunt.initConfig({
        copy: {
            dist: {
                files: [{
                    expand: true,
                    src: '**',
                    cwd: 'app/assets/partials/',
                    dest: 'static/partials/',
                    filter: 'isFile'
                }]
            }
        },
        concat: {
            dist: {
                files: {
                    'static/js/app.min.js': [
                        'bower_components/jquery/dist/jquery.js',
                        'bower_components/moment/moment.js',
                        'bower_components/angular/angular.js',
                        'bower_components/angular-sanitize/angular-sanitize.js',
                        'bower_components/angular-resource/angular-resource.js',
                        'bower_components/angular-messages/angular-messages.js',
                        'bower_components/angular-ressource/angular-ressource.js',
                        'bower_components/angular-route/angular-route.js',
                        'bower_components/ngstorage/ngStorage.js',
                        'app/assets/js/app.js',
                        'app/assets/js/controllers/*.js',
                        'app/assets/js/directives/*.js',
                        'app/assets/js/resources/*.js',
                        'app/assets/js/services/*.js',
                        'app/assets/js/run.js',
                        'app/assets/js/config.js',
                        'app/assets/js/routes.js',
                    ]
                }
            }
        },
        sass: {
            dist: {
                options: {
                    style: 'expanded'
                },
                files: {
                    'static/css/styles.min.css': [
                        'app/assets/scss/base.scss'
                    ]
                }
            }
        },
        watch: {
            files: ['app/assets/**/*.*'],
            tasks: ['concat', 'sass', 'copy']
        }
    });

    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-concat');

    grunt.registerTask('default', ['sass', 'copy', 'concat']);

};
