function deleteTexture(element, texture_id) 
{
    $.ajax({
		url: '',
		type: 'POST',
		data: {
			deleteTexture: true,
			texture_id: texture_id,
			csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
		},
		success: () => {
			element.parentElement.remove();
		}
	});
}