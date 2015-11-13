var awsIot = require('aws-iot-device-sdk');

var thingShadows = awsIot.thingShadow({
   keyPath: '/root/awsCerts/private.pem.key',
  certPath: '/root/awsCerts/certificate.pem.crt',
    caPath: '/root/awsCerts/root-CA.crt',
  clientId: 'myAwsClientId',
    region: 'eu-west-1'
});

//
// Thing shadow state
//
var FirstThingState = {"state": null};

//
// Client token value returned from thingShadows.update() operation
//
var clientTokenUpdate;

thingShadows.on('connect', function() {
	console.log('connected to things instance, registering thing name...');
//
// After connecting to the AWS IoT platform, register interest in the
// Thing Shadow named 'FirstThing'.
//
    thingShadows.register( 'FirstThing' );
	console.log('>FirstThing< registered. Waitung for 2 seconds...');
//
// 2 seconds after registering, update the Thing Shadow named 
// 'FirstThing' with the latest device state and save the clientToken
// so that we can correlate it with status or timeout events.
//
// Note that the delay is not required for subsequent updates; only
// the first update after a Thing Shadow registration using default
// parameters requires a delay.  See API documentation for the update
// method for more details.
//
    setTimeout( function() {
       clientTokenUpdate = thingShadows.update('FirstThing', FirstThingState);
       }, 2000 );
    });

thingShadows.on('status', 
    function(thingName, stat, clientToken, stateObject) {
       console.log('received '+stat+' on '+thingName+': '+
                   JSON.stringify(stateObject));
    });

thingShadows.on('delta', 
    function(thingName, stateObject) {
       console.log('received delta '+' on '+thingName+': '+
                   JSON.stringify(stateObject));
    });

thingShadows.on('timeout',
    function(thingName, clientToken) {
       console.log('received timeout '+' on '+operation+': '+
                   clientToken);
    });