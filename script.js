document.addEventListener('DOMContentLoaded', () => {
    const mapSections = document.querySelectorAll('.map-section');
  
    mapSections.forEach(section => {
      // Preload street view images for smoother animation
      const imgTop = new Image();
      imgTop.src = section.dataset.topView;
      const imgStreet = new Image();
      imgStreet.src = section.dataset.streetView;
  
      section.style.backgroundImage = `url(${section.dataset.topView})`;
  
      section.addEventListener('mouseenter', () => {
        section.style.backgroundImage = `url(${section.dataset.streetView})`;
      });
  
      section.addEventListener('mouseleave', () => {
        section.style.backgroundImage = `url(${section.dataset.topView})`;
      });
    });
  });
  
  function changeImage(element, newImageSrc) {
    element.querySelector('img').src = newImageSrc;
  }
  
  function resetImage(element, originalImageSrc) {
    element.querySelector('img').src = originalImageSrc;
  }
  