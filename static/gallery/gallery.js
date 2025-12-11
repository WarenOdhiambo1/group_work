// // Gallery Image Loading Handler
// document.addEventListener('DOMContentLoaded', function() {
//     const galleryImages = document.querySelectorAll('.gallery-item img');
    
//     galleryImages.forEach(img => {
//         const galleryItem = img.closest('.gallery-item');
        
//         // Add loading class
//         galleryItem.classList.add('loading');
        
//         // Handle successful image load
//         img.addEventListener('load', function() {
//             galleryItem.classList.remove('loading');
//         });
        
//         // Handle image load error
//         img.addEventListener('error', function() {
//             galleryItem.classList.remove('loading');
//             // Set fallback image
//             this.src = 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&h=300&q=80';
//             this.alt = 'Adventure Photo';
//         });
        
//         // If image is already cached and loaded
//         if (img.complete) {
//             galleryItem.classList.remove('loading');
//         }
//     });
// });