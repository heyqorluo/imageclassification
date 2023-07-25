// const url = 'http://127.0.0.1:8000/text_test'
// const url ="http://127.0.0.1:8000/classify_image2";
const url = 'https://upx3yb0685.execute-api.eu-west-2.amazonaws.com/api/classify_image2/'

// Add a click event listener to the button
document.getElementById("myButton").addEventListener("click", function() {
  // alert("Button Clicked!!");
  console.log("Classifying image...");
  // sendingtext();
  // sendingimage();
  uploadImage();
  document.getElementById("result").innerHTML = "";
  document.getElementsByClassName("loader")[0].style.display = "block";
  
});

var imBytes;
var imageInput = document.getElementById("imagePreview");
var fileInput = document.getElementById("input-file");

fileInput.onchange = function(){
  imageInput.src = URL.createObjectURL(fileInput.files[0]);
  document.getElementById("result").innerHTML = "Result output";
};

let file;
let result;

imageInput.onload = function(){
  file = fileInput.files[0];

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

async function uploadImage() {
  const base64Image = await toBase64(file);
  // console.log(base64Image);

  const payload = {
      filename: file.name,
      image: base64Image,
  };

  const response = await fetch(url, {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
  })
  .then(function(res){ return res.json(); })
  // .then(function(data){ alert( JSON.stringify( data ) );
  // result = data;})
  .then(function(data){result = data;});
  ReportResult();
};


function toBase64(file) {
  return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
          // Convert the Data URL to Base64 string, remove prefix
          const base64String = reader.result.split(",")[1];
          resolve(base64String);
      };
      reader.onerror = (error) => reject(error);
  });
}

function ReportResult(){
  let list = result["Result:"]["prediction_result"];
  let ResultfromList = Object.entries(list)[0];
  console.log(ResultfromList);
  document.getElementsByClassName("loader")[0].style.display = "none";
  document.getElementById("result").innerHTML += "Result output"+"<br>"+"<br>" + ResultfromList + "%";
}