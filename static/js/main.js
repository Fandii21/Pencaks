// const previewImage = () => {
//     let file = document.querySelector("#fileInput");
//     let picture = document.querySelector(".picture");
//     let message = document.querySelector(".message");
//     let btnUpload = document.querySelector(".btnUpload");
//     picture.src = window.URL.createObjectURL(file.files[0]);

//     let regex = new RegExp("[^.]+$");
//     fileExtension = file.files[0].name.match(regex)[0];
//     if (fileExtension === "JPG" || fileExtension === "JPEG" || fileExtension === "png") {
//         btnUpload.style.display = "block";
//         message.innerHTML = "Deteksi Gambar";
//     } else {
//         picture.src = "/static/img/none.png";
//         btnUpload.style.display = "none";
//         message.innerHTML = "<b>" + fileExtension + "</b> file is not allowed.<br/>Choose a .jpg or .png only";
//     }
// };

// function previewImage() {
//     var fileInput = document.getElementById('fileInput');
//     var imagePreview = document.getElementById('imagePreview');

//     var file = fileInput.files[0];
//     var reader = new FileReader();

//     reader.onload = function (e) {
//         imagePreview.src = e.target.result;
//     }

//     reader.readAsDataURL(file);

// }

const previewImage = () => {
    let file = document.querySelector("#fileInput");
    let picture = document.querySelector(".picture");
    let message = document.querySelector(".message");
    let btnUpload = document.querySelector(".btnUpload");
    picture.src = window.URL.createObjectURL(file.files[0]);

    let regex = new RegExp("[^.]+$");
    fileExtension = file.files[0].name.match(regex)[0];
    if (fileExtension === "JPG" || fileExtension === "jpg" || fileExtension === "png") {
        btnUpload.style.display = "block";
        message.innerHTML = "Deteksi Gambar";
    } else {
        picture.src = "/static/img/none.png";
        btnUpload.style.display = "none";
        message.innerHTML = "<b>" + fileExtension + "</b> file is not allowed.<br/>Choose a .jpg or .png only";
    }
};