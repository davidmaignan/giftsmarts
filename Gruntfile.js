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
                        'bower_components/bootstrap-sass/assets/javascripts/bootstrap.min.js',
                        'bower_components/angular/angular.js',
                        'bower_components/angular-sanitize/angular-sanitize.js',
                        'bower_components/angular-resource/angular-resource.js',
                        'bower_components/angular-messages/angular-messages.js',
                        'bower_components/angular-ressource/angular-ressource.js',
                        'bower_components/angular-route/angular-route.js',
                        'bower_components/angular-isotope/demo/scripts/angular-isotope.js',
                        'bower_components/ngstorage/ngStorage.js',
                        'bower_components/packery/dist/packery.pkgd.js',
                        // isotope
                        'bower_components/isotope/js/layout-mode.js',
                        'bower_components/isotope/js/item.js',
                        'bower_components/isotope/js/isotope.js',
                        'bower_components/isotope/js/layout-modes/fit-rows.js',
                        'bower_components/isotope/js/layout-modes/vertical.js',
                        // isotope masonry
                        'bower_components/masonry/masonry.js',
                        'bower_components/isotope/js/layout-modes/masonry.js',
                        // layout modes
                        'bower_components/isotope-cells-by-column/cells-by-column.js',
                        'bower_components/isotope-cells-by-row/cells-by-row.js',
                        'bower_components/isotope-fit-columns/fit-columns.js',
                        'bower_components/isotope-horizontal/horizontal.js',
                        'bower_components/isotope-masonry-horizontal/masonry-horizontal.js',
                        // isotope packery
                        'bower_components/packery/js/rect.js',
                        'bower_components/packery/js/packer.js',
                        'bower_components/packery/js/item.js',
                        'bower_components/packery/js/packery.js',
                        'bower_components/isotope-packery/packery-mode.js',
                        'app/assets/js/app.js',
                        'app/assets/js/controllers/*.js',
                        'app/assets/js/directives/*.js',
                        'app/assets/js/resources/*.js',
                        'app/assets/js/services/*.js',
                        'app/assets/js/run.js',
                        'app/assets/js/config.js',
                        'app/assets/js/routes.js',
                        'app/assets/js/profile.js'
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
