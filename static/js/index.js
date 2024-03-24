$(document).ready(function() {
    // Access restaurants data passed from Flask template
    var restaurants = {{ restaurants | tojson }};
  
    // Loop through restaurants and dynamically create cards
    $.each(restaurants, function(index, restaurant) {
      var card = $('<div class="restaurant-card">');
      card.append(`<h3>${restaurant.name}</h3>`);  // Example: Access restaurant name
      // Add more content to the card based on your database schema (e.g., image, description)
      card.appendTo('.restaurant-container');
    });
  });
  