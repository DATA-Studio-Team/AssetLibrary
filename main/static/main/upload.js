function updatePreviewModel(el) 
{
    document.getElementById("preview").src = URL.createObjectURL(el.files[0]);
}

function updatePreviewTexture(el) 
{
    let preview = document.getElementById("texturesPreview");
    preview.innerHTML = "";

    const template = document.querySelector('#textureContainer');

    for (const file of el.files)
    {
        let newContainer = template.content.cloneNode(true);
        newContainer.querySelector('img').src = URL.createObjectURL(file);
        newContainer.querySelector('h6').textContent = file.name;
        preview.appendChild(newContainer);
    }
}