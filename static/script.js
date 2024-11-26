async function calcular() {
    const nombre = document.getElementById("nombre").value; // Capturar el nombre
    const genero = document.getElementById("genero").value;
    const peso = document.getElementById("peso").value;
    const altura = document.getElementById("altura").value;
    const edad = document.getElementById("edad").value;
    const actividad = document.getElementById("actividad").value;

    const datos = { nombre, genero, peso, altura, edad, actividad }; // Incluir el nombre en los datos

    const respuesta = await fetch('/calcular', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(datos) // Enviar los datos como JSON
    });

    const resultado = await respuesta.json();
    if (respuesta.ok) {
        document.getElementById("resultado").innerText = 
            `Tasa Metabolica Basal: ${resultado.calorias_diarias}`;
    } else {
        document.getElementById("resultado").innerText = 
            `Error: ${resultado.error}`;
    }
}

async function toggleMostrarHistorial() {
    const contenedorHistorial = document.getElementById("historial");

    if (contenedorHistorial.style.display === "none" || contenedorHistorial.style.display === "") {
        // Mostrar historial y cargar los datos desde el backend
        contenedorHistorial.style.display = "block";

        try {
            const respuesta = await fetch('/historial');
            
            // Verificar si la respuesta es exitosa
            if (!respuesta.ok) {
                throw new Error(`Error al obtener el historial: ${respuesta.status}`);
            }

            const historial = await respuesta.json();
            contenedorHistorial.innerHTML = ""; // Limpiar contenido previo

            if (historial.length === 0) {
                contenedorHistorial.innerHTML = "<p>No hay cálculos registrados aún.</p>";
                return;
            }

            // Mostrar los registros en el historial
            historial.forEach(item => {
                const entrada = `
                    <div class="historial-item">
                        <p><strong>Nombre:</strong> ${item.nombre}</p>
                        <p><strong>Fecha:</strong> ${item.fecha}</p>
                        <p><strong>Género:</strong> ${item.genero}</p>
                        <p><strong>Peso:</strong> ${item.peso} kg</p>
                        <p><strong>Altura:</strong> ${item.altura} cm</p>
                        <p><strong>Edad:</strong> ${item.edad} años</p>
                        <p><strong>Actividad:</strong> ${item.actividad}</p>
                        <p><strong>Calorías:</strong> ${item.calorias} kcal</p>
                    </div>
                    <hr>
                `;
                contenedorHistorial.innerHTML += entrada;
            });
        } catch (error) {
            console.error(error);
            alert("Hubo un problema al cargar el historial.");
        }
    } else {
        // Ocultar historial
        contenedorHistorial.style.display = "none";
    }
}
async function borrarHistorial() {
    const respuesta = await fetch('/borrar_historial', {
        method: 'DELETE'
    });

    const resultado = await respuesta.json();
    alert(resultado.mensaje);
    document.getElementById("historial").innerHTML = ""; // Limpiar el historial
}

