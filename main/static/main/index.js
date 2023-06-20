function changeFavorite(element, id) 
{
    $.ajax({
		url: '',
		type: 'POST',
		data: {
            setAsFavourite: element.checked,
            id: id,
			csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
		}
	});
}