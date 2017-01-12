
////////////////////////////////
		//Setup//
////////////////////////////////

// Plugins
var gulp = require('gulp'),
    pjson = require('./package.json'),
    gutil = require('gulp-util'),
    less = require('gulp-less'),
    autoprefixer = require('gulp-autoprefixer'),
    rigger = require('gulp-rigger'),
    cssnano = require('gulp-cssnano'),
    rename = require('gulp-rename'),
    del = require('del'),
    plumber = require('gulp-plumber'),
    pixrem = require('gulp-pixrem'),
    uglify = require('gulp-uglify'),
    imagemin = require('gulp-imagemin'),
    exec = require('child_process').exec,
    runSequence = require('run-sequence'),
    rimraf = require('gulp-rimraf'),
    browserSync = require('browser-sync').create(),
    // cleanCSS = require('gulp-clean-css'),
    reload = browserSync.reload;


// Relative paths function
var pathsConfig = function () {
  this.app = "./apps";

  return {
    app: this.app,
    templates: this.app + '/templates',
    css: this.app + '/static/css',
    less: this.app + '/static/less',
    fonts: this.app + '/static/fonts',
    images: this.app + '/static/img',
    js: this.app + '/static/js'
  }
};

var paths = pathsConfig();

////////////////////////////////
		//Tasks//
////////////////////////////////

// Styles autoprefixing and minification
gulp.task('styles', function() {
  return gulp.src(paths.less + "/*.less")
    .pipe(less().on('error', gutil.log)) // Compile
    //.pipe(cleanCSS())
    .pipe(plumber()) // Checks for errors
    .pipe(autoprefixer({browsers: ['last 2 version']})) // Adds vendor prefixes
    .pipe(pixrem())  // add fallbacks for rem units
    .pipe(gulp.dest(paths.css))
    .pipe(rename({ suffix: '.min' }))
    .pipe(cssnano()) // Minifies the result
    .pipe(gulp.dest(paths.css));
});

// Javascript minification
gulp.task('scripts', function() {
  return gulp.src(paths.js + '/project.js')
    .pipe(plumber()) // Checks for errors
    .pipe(uglify()) // Minifies the js
    .pipe(rename({ suffix: '.min' }))
    .pipe(gulp.dest(paths.js));
});

// Image compression
gulp.task('imgCompression', function(){
  return gulp.src(paths.images + '/*')
    .pipe(imagemin()) // Compresses PNG, JPEG, GIF and SVG images
    .pipe(gulp.dest(paths.images))
});

// Run django server
gulp.task('server', function() {
  exec('python manage.py runserver 0.0.0.0:8000', function (err, stdout, stderr) {
    console.log(stdout);
    console.log(stderr);
  });
});

// Browser sync server for live reload
gulp.task('browserSync', function() {
    browserSync.init(
      [paths.css + "/*.css", paths.js + "*.js", paths.templates + '*.html'], {
        proxy:  "0.0.0.0:8000"
    });
});

// Default task
gulp.task('default', function() {
    // runSequence(['styles', 'scripts', 'imgCompression'], 'server', 'browserSync');
    runSequence(['styles', 'scripts']);
});

////////////////////////////////
		//Watch//
////////////////////////////////

// Watch
gulp.task('watch', ['default'], function() {

  gulp.watch(paths.less + '/**/*.less', ['styles']);
  gulp.watch(paths.js + '/**/*.js', ['scripts']);
  // gulp.watch(paths.js + '/*.js', ['scripts']).on("change", reload);
  // gulp.watch(paths.images + '/*', ['imgCompression']);
  // gulp.watch(paths.templates + '/**/*.html').on("change", reload);

});
