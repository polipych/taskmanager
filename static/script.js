
// function show_delete_alert(item_id, item_title) {
//     alert("Будет удалена запись " + item_id + " с заголовком " + item_title);
// };

function show_delete_alert(item_id, csrf_token) {
    alert("Будет удалена запись " + item_id);

    call_delete_request("" + item_id, "" + csrf_token)
};

function call_delete_request(url, csrf_token) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("DELETE", url, true);
    xhttp.setRequestHeader("X-CSRFToken", "" + csrf_token.toString());
    xhttp.send();
    window.location.reload(true);
    window.location.reload();
    location.reload();
    $('#myModal').modal('hide')
};


// function show_delete_div(item_id, item_title, csrf_token) {
//     let div = document.createElement('div');
//     div.innerHTML = "<strong>Будет удалена запись номер " + item_id + "</strong> С заголовком.";
//     let p = document.createElement('p')
//     p.textContent = item_title
//     div.append(p)

//     document.body.append(div);
//     setTimeout(() => div.remove(), 1000); // Уничтожть элемент спустя какое-то время

//     call_delete_request("/delete/" + item_id, "" + csrf_token)
// };

// function show_edit_tab(url) {
//     window.open(url, '_blank');
// };

// function show_delete_modal(url, csrf_token) {
//     $('#myModal').modal('show');
// };

// function call_get_dashboard_data(csrf_token) {
//     url = "/dashboard_data/"

//     var xhr = new XMLHttpRequest();
//     xhr.open('GET', url, false);
//     xhr.setRequestHeader("X-CSRFToken", "" + csrf_token.toString());
//     xhr.send(null);
//     return xhr.responseText
// };