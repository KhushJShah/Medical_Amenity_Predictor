document.addEventListener('DOMContentLoaded', function() {
    const map = document.getElementById('interactiveMap');
    document.querySelectorAll('.location-pointer').forEach(pointer => {
        pointer.addEventListener('mouseenter', function() {
            const location = this.getAttribute('data-location');
            const rect = this.getBoundingClientRect();
            
            // Calculate scale and position for zoom
            const scale = 2; // Example scale factor
            const offsetX = -rect.left * (scale - 1);
            const offsetY = -rect.top * (scale - 1);
            
            map.style.transform = `scale(${scale}) translate(${offsetX}px, ${offsetY}px)`;
        });

        pointer.addEventListener('mouseleave', function() {
            map.style.transform = 'scale(1) translate(0px, 0px)';
        });
    });
});
