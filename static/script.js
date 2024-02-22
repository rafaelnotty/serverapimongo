document.getElementById('loadButton').addEventListener('click', function() {
    // Actualizar el estado a 'Cargando...'
    document.getElementById('status').innerText = 'Cargando...';

    // Simular un proceso de carga
    setTimeout(function() {
        // Actualizar el estado a 'Procesamiento completado'
        document.getElementById('status').innerText = 'Procesamiento completado';
    }, 3000); // 3000 milisegundos = 3 segundos
});
