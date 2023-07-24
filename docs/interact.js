// const url = 'http://127.0.0.1:8000/text_test'
const url ="http://127.0.0.1:8000/classify_image";
// const url = 'https://upx3yb0685.execute-api.eu-west-2.amazonaws.com/api/text_test/'

// Add a click event listener to the button
document.getElementById("myButton").addEventListener("click", function() {
  // alert("Button Clicked!!");
  console.log("hello world");
  // sendingtext();
  sendingimage();
});

var imBytes;
var imageInput = document.getElementById("imagePreview");
var fileInput = document.getElementById("input-file");

fileInput.onchange = function(){
  imageInput.src = URL.createObjectURL(fileInput.files[0]);
};

imageInput.onload = function(){
  var file = fileInput.files[0];
  var reader = new FileReader();
  reader.onloadend = function() {
    var arrayBuffer = reader.result;
    console.log('RESULT', reader.result);
    console.log('FILE', file);
    imBytes = new Uint8Array(arrayBuffer);
    console.log('imBytes', imBytes);
    };
  reader.readAsArrayBuffer(file);
};

const sendingtext = function () {
  var payload = {
    a: 1,
    b: 2
};

fetch(url,
{
    method: "POST",
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify( payload )
})
.then(function(res){ return res.json(); })
.then(function(data){ alert( JSON.stringify( data ) ); });
};


const sendingimage = function () {
// Encode the image data to Base64.
const imB64  = imBytes.toString('base64');

// Prepare the JSON payload.
const payload = JSON.stringify({ "image": imB64 });

// Prepare the headers for the HTTP request.
const headers = {
  "Content-Type": "application/json",
  "Accept": "text/plain"
};
fetch(url,
  {
      method: "POST",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json"
      },
      body: JSON.stringify( payload )
  })
  .then(function(res){ return res.json(); })
  .then(function(data){ alert( JSON.stringify( data ) ); });
};

