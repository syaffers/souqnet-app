if (window.location.pathname === "/") {
    Webcam.set({
        width: 480,
        height: 360,
        image_format: 'png'
    });
    Webcam.attach('#camera');

    document.getElementById('snap').addEventListener('click', function() {
        Webcam.snap(function(data) {
            document.getElementById('image-data').value = data;
            document.getElementById('upload-form').submit();
        });
    });
}
