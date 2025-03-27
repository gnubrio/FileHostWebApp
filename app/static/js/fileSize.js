function displayFileSize() {
    const defaultSize = 0;

    if (!fileSize) {
        return `${defaultSize} KB`;
    }

    var sizeInKb = fileSize / 1024;

    if (sizeInKb > 1024) {
        return `${(sizeInKb / 1024).toFixed(2)} MB`;
    } else {
        return `${sizeInKb.toFixed(2)} KB`;
    }
}

var newValue = displayFileSize(fileSize);
document.getElementById("fileSize").textContent = newValue;
