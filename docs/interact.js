function uploading() {
document.getElementById("uploadrec").addEventListener('click', function(event) {
    const file = event.target.files[0];
  
    if (file) {
      const reader = new FileReader();
  
      reader.onload = function() {
        const imagePreview = document.getElementById('imagePreview');
        imagePreview.innerHTML = `<img src="${reader.result}" alt="Uploaded Image" />`;
      };
  
      reader.readAsDataURL(file);
    }
  });
}