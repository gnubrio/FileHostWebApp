const fileInput = document.getElementById("file");

function changeLabelText() {
    var fileName = fileInput.files[0]?.name;

    if (!fileName) {
        return;
    }

    var label = document.querySelector("label[for='file']");
    var maxLength = label.innerText.length;

    if (fileName.length >= maxLength) {
        let dots = "...";
        fileName = fileName.slice(0, (maxLength - dots.length));
        fileName += dots;
    }

    label.innerText = fileName;
}

fileInput.addEventListener("change", changeLabelText, false);
