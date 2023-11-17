document.addEventListener('DOMContentLoaded', function() {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    var video = document.getElementById('webcam');
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    var streaming = false;

    navigator.mediaDevices.getUserMedia({ video: true, audio: false })
    .then(function(stream) {
        video.srcObject = stream;
        video.play();
    })
    .catch(function(err) {
        console.log("An error occurred: " + err);
    });

    video.addEventListener('canplay', function(ev) {
        if (!streaming) {
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            streaming = true;
        }
    }, false);

    function sendFrame() {
        if (streaming) {
            context.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
            var data = canvas.toDataURL('image/jpeg');
            data = data.split(',')[1]; // Remove the Data URL prefix and send only the base64 string
            socket.emit('frame', data);
        }
        requestAnimationFrame(sendFrame);
    }

    video.addEventListener('play', function() {
        // Start sending frames when video starts playing
        requestAnimationFrame(sendFrame);
    }, false);
});
