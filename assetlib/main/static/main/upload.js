function previewModelSet(el) {
    
    var tgt = el.target || window.event.srcElement, files = tgt.files;

    if (FileReader && files && files.length) {
        var fr = new FileReader();

        fr.onload = function () {
            document.getElementById("preview").src = fr.result;
        }

        fr.readAsDataURL(files[0]);
    }

}