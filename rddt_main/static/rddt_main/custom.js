function reply(obj, comment_id) {
    var url = "reply/?replied_comment=" + comment_id;

    fetch(url)
    .then((response) => response.text())
    .then((html) => {
        obj.hidden = true;
        var new_html = '<div>' + obj.outerHTML + html + '</div>';
        obj.outerHTML = new_html;
    })
    .catch((error) => {
        console.warn(error);
    });
}

function close_form(obj) {
    obj = obj.parentElement.parentElement.parentElement;
    obj.children[0].hidden = false;
    obj.outerHTML = obj.children[0].outerHTML;
}
