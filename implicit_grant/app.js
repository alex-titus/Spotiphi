/**
 * This is an example of a basic node.js script that performs
 * the Implicit Grant oAuth2 flow to authenticate against
 * the Spotify Accounts.
 *
 * For more information, read
 * https://developer.spotify.com/web-api/authorization-guide/#implicit_grant_flow
 */

var express = require('express'); // Express web server framework
var client_id = '67c9bdb789854efc9b20b4c4c06ca0cb'; // Your client id
var client_secret = '22132f38bf3e47b794903f9302b5be8e'; // Your secret
var redirect_uri = 'http://localhost:8888/callback'; // Your redirect uri
var app = express();
app.use(express.static(__dirname + '/public'));
console.log('Listening on 8888');
app.listen(8888);
