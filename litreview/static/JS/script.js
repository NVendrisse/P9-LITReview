
function confirmDelete(e) {

    Swal.fire({
        title: 'Confirmation de la suppression',
        text: 'Cette action est définitive!',
        showCancelButton: true,
        showConfirmButton: true
    }).then(result => {
        if (result.isConfirmed) {
            const id = e.target.attributes.item_id.nodeValue;
            const type = e.target.attributes.item_type.nodeValue;
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            fetch("/delete/" + type + "/" + id + "/", {
                method: "POST",
                credentials: 'same-origin',
                headers: { 'X-CSRFToken': csrftoken }
            })

        }
    })
}


document.querySelectorAll(".js-delete").forEach((element) => {
    element.addEventListener("click", (e) => {
        confirmDelete(e)
    })
})
