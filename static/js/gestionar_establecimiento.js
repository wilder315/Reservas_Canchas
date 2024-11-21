document.addEventListener("DOMContentLoaded", function () {
    // Inicializar DataTable
    $('#establecimientosTable').DataTable({
        pageLength: 8,
        language: {
            search: "Buscar:",
            emptyTable: "No hay establecimientos disponibles."
        }
    });
});

// Función para abrir el modal
function openModal(type, id = null, nombre = '', descripcion = '', latitud = '', longitud = '', apertura = '', cierre = '') {
    const modalTitle = document.getElementById("establecimientoModalLabel");
    const formAction = document.getElementById("establecimientoForm");

    if (type === "add") {
        modalTitle.innerText = "Agregar Establecimiento";
        formAction.action = urlInsertarEstablecimiento;
        limpiarModal();
    } else if (type === "edit") {
        modalTitle.innerText = "Editar Establecimiento";
        formAction.action = urlActualizarEstablecimiento;

        document.getElementById("establecimientoId").value = id;
        document.getElementById("nombre").value = nombre;
        document.getElementById("descripcion").value = descripcion;
        document.getElementById("ubicacion_latitud").value = latitud;
        document.getElementById("ubicacion_longitud").value = longitud;
        document.getElementById("horario_apertura").value = apertura;
        document.getElementById("horario_cierre").value = cierre;
    }

    const modal = new bootstrap.Modal(document.getElementById("establecimientoModal"));
    modal.show();
}

// Función para limpiar los campos del modal
function limpiarModal() {
    document.getElementById("establecimientoForm").reset();
    document.getElementById("establecimientoId").value = "";
}

// Función para enviar el formulario
document.getElementById("establecimientoForm").addEventListener("submit", function (event) {
    event.preventDefault();
    const form = this;
    const url = form.action;
    const formData = new FormData(form);

    fetch(url, {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message || "Operación exitosa");
            location.reload();
        } else {
            alert(data.message || "Ocurrió un error");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Ocurrió un error en la operación.");
    });
});
