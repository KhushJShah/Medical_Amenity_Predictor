document.addEventListener('DOMContentLoaded', () => {
  const coverImages = document.querySelectorAll('#cover > img'); // Select the images within #cover

  coverImages.forEach(img => {
      img.addEventListener('mouseenter', () => {
          changeImage(img, img.getAttribute('data-street-view')); // Change to street view
      });

      img.addEventListener('mouseleave', () => {
          resetImage(img, img.src); // Reset to original image
      });
  });
});

function changeImage(img, newImageSrc) {
  img.src = newImageSrc;
}

function resetImage(img, originalImageSrc) {
  img.src = originalImageSrc.replace('streets', 'map_aligned'); // Reset to top view
}
