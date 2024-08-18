// const url = 'http://127.0.0.1:8000/text_test'
// const url ="http://127.0.0.1:8000/classify_image2";
// const url = 'https://upx3yb0685.execute-api.eu-west-2.amazonaws.com/api/classify_image2/'
const url = 'https://24664vwhl1.execute-api.eu-west-2.amazonaws.com/api/classify_image2/'

let file;
let result;
let list;
let listarray = [];

// Add a click event listener to the button
document.getElementById("myButton").addEventListener("click", function() {
  // alert("Button Clicked!!");
  console.log("Classifying image...");
  // sendingtext();
  // sendingimage();
  listarray = [];
  uploadImage();
  document.getElementById("result").innerHTML = "";
  document.getElementsByClassName("loader")[0].style.display = "block";
});

var imBytes;
var imageInput = document.getElementById("imagePreview");
var fileInput = document.getElementById("input-file");

fileInput.onchange = function(){
  imageInput.src = URL.createObjectURL(fileInput.files[0]);
  document.getElementById("result").innerHTML = "Result will be shown here.";
};


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
  list = result["Result:"]["prediction_result"];
  let ResultfromList = Object.entries(list)[0];
  let regex = /[^a-zA-Z0-9]/g;
  ResultfromList[0] = ResultfromList[0].replace(regex, "");
  document.getElementsByClassName("loader")[0].style.display = "none";
  document.getElementById("result").innerHTML += "This picture has " + ResultfromList[1] + "% chance of being a " + ResultfromList[0] + ".";
  cleanData();
  PlotBarChart();
}
function cleanData(){
  let regex = /[^a-zA-Z0-9]/g;
  let Arraylist = Object.entries(list);
  Arraylist.forEach(function(item){
    item[0] = item[0].replace(regex, "");
  });
  for (var i in Arraylist){
    listarray.push([Arraylist[i][0], Arraylist[i][1]]);
  }
  console.log(listarray);
}

function PlotBarChart(){
var xValues = [];
var yValues = [];
var barColors = ["#ECD0D0", "#80BA77","blue","orange","brown"];

for (var i in listarray){
  xValues.push(listarray[i][0]);
  yValues.push(listarray[i][1]);
}
console.log(xValues);
console.log(yValues);

new Chart("myChart", {
  type: "bar",
  data: {
    labels: xValues,
    datasets: [{
      backgroundColor: barColors,
      data: yValues
    }]
  },
  options: {
    legend: {display: false},
    title: {
      display: true,
      text: "Classification Result",
      fontSize: 16,
    },
    scales: {
      yAxes: [{
        ticks: {
          beginAtZero: true,
          min: 0,
          max: 100,
          stepSize: 10,
        }
      }]
    }
  }
});
}
