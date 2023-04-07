function updatePreviewModel(el) 
{

    if (FileReader && el.files && files.length) 
    {
        var fr = new FileReader();

        fr.onload = function () 
        {
            document.getElementById("preview").src = fr.result;
        }

        fr.readAsDataURL(el.files[0]);
    }
}

function updatePreviewTexture(el) 
{

}