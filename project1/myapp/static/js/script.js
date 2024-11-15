// carousel js code starts 
document.querySelectorAll('.items-btn').forEach((button, index) => {
  button.addEventListener('click', function () {
    // Remove the 'active' class from all buttons
    document.querySelectorAll('.items-btn').forEach(btn => btn.classList.remove('active'));

    // Add the 'active' class to the clicked button
    this.classList.add('active');

    // Select the carousel element         
    const carousel = document.querySelector('#carouselExample');

    // Move the carousel to the corresponding item
    const bsCarousel = new bootstrap.Carousel(carousel); // Initialize the Bootstrap Carousel
    bsCarousel.to(index); // Move to the slide matching the clicked button
  });
});

// carousel code ends 

