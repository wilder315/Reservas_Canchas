function toggleForm() {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const formTitle = document.getElementById('form-title');
    const formDescription = document.getElementById('form-description');
    const toggleLink = document.getElementById('toggle-form');

    if (loginForm.style.display === 'none') {
        loginForm.style.display = 'block';
        registerForm.style.display = 'none';
        formTitle.textContent = 'Bienvenido';
        formDescription.textContent = 'Ingrese sus credenciales para acceder al sistema';
        toggleLink.textContent = '¿Nuevo aquí? Regístrate';
    } else {
        loginForm.style.display = 'none';
        registerForm.style.display = 'block';
        formTitle.textContent = 'Crear Cuenta';
        formDescription.textContent = 'Complete la información para registrarse';
        toggleLink.textContent = '¿Ya tienes cuenta? Inicia sesión';
    }
}

function procesar_registro() {
    const fullName = document.getElementById('fullName').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('registerPassword').value.trim();

    if (fullName === '' || email === '' || password === '') {
        mostrarError("warning", "Registro incompleto", "Por favor complete todos los campos.");
        return;
    }

    fetch('/procesar_registro', {
        method: 'POST',
        headers: { 'Content-type': 'application/json' },
        body: JSON.stringify({ fullName, email, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.registrado) {
            mostrarAlerta("success", "Registro exitoso", "Su cuenta ha sido creada con éxito.");
            toggleForm(); // Cambiar al formulario de login
        } else {
            mostrarError("error", "Registro fallido", data.mensaje);
        }
    })
    .catch(error => {
        mostrarError("error", "Error al registrarse", error);
    });
}
