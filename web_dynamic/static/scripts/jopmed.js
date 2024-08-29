// /* global $ */

// $(document).ready(function () {
//   const selectedStates = {};
//   const selectedCities = {};

//   $('input[type="checkbox"]').change(function () {
//     const id = $(this).data('id');
//     const name = $(this).data('name');
//     if ($(this).is(':checked')) {
//       if ($(this).closest('li').parent().parent().is('li')) {
//         selectedCities[id] = name;
//       } else {
//         selectedStates[id] = name;
//       }
//     } else {
//       if ($(this).closest('li').parent().parent().is('li')) {
//         delete selectedCities[id];
//       } else {
//         delete selectedStates[id];
//       }
//     }
//     updateLocations();
//   });

//   function updateLocations () {
//     const locations = Object.values(selectedStates).concat(Object.values(selectedCities));
//     $('div.locations h4').text(locations.join(', '));
//   }

//   $.get('http://0.0.0.0:5001/api/v1/status/', function (data) {
//     if (data.status === 'OK') {
//       $('#api_status').addClass('available');
//     } else {
//       $('#api_status').removeClass('available');
//     }
//   }).fail(function () {
//     console.error('Failed to fetch API status');
//   });

//   function fetchPlaces (data) {
//     $.ajax({
//       url: 'http://0.0.0.0:5001/api/v1/places_search/',
//       type: 'POST',
//       contentType: 'application/json',
//       data: JSON.stringify(data),
//       success: function (data) {
//         console.log('API Response:', data); // Log the API response
//         $('section.places').empty();
//         for (const place of data) {
//           console.log('Place:', place); // Log each place
//           const article = $('<article></article>');
//           const titleBox = $('<div class="title_box"></div>');
//           titleBox.append(`<h2>${place.name || 'N/A'}</h2>`);
//           titleBox.append(`<div class="price_by_night">$${place.price_by_night || 'N/A'}</div>`);
//           article.append(titleBox);

//           const information = $('<div class="information"></div>');
//           information.append(`<div class="max_guest">${place.max_guest || 'N/A'} Guest${place.max_guest !== 1 ? 's' : ''}</div>`);
//           information.append(`<div class="number_rooms">${place.number_rooms || 'N/A'} Bedroom${place.number_rooms !== 1 ? 's' : ''}</div>`);
//           information.append(`<div class="number_bathrooms">${place.number_bathrooms || 'N/A'} Bathroom${place.number_bathrooms !== 1 ? 's' : ''}</div>`);
//           article.append(information);

//           const userDiv = $('<div class="user"></div>');
//           const user = place.user || {};
//           userDiv.append(`<b>Owner:</b> ${user.first_name || 'N/A'} ${user.last_name || 'N/A'}`);
//           article.append(userDiv);

//           const description = $('<div class="description"></div>');
//           description.append(place.description || 'N/A');
//           article.append(description);

//           const reviews = $('<div class="reviews" style="margin-top: 40px;"></div>');
//           reviews.append(`<h2 style="font-size: 16px; border-bottom: 1px solid #DDDDDD;">Reviews <span class="toggle-reviews" data-place-id="${place.id}">show</span></h2>`);
//           reviews.append('<ul class="review-list" style="list-style: none;"></ul>');
//           article.append(reviews);

//           $('section.places').append(article);
//         }
//       },
//       error: function () {
//         console.error('Failed to fetch places');
//       }
//     });
//   }

//   // Initial fetch of places
//   fetchPlaces({});

//   // Event handler for button click to fetch places based on selected amenities, states, and cities
//   $('button').click(function () {
//     const amenities = [];
//     $('input[type="checkbox"]:checked').each(function () {
//       amenities.push($(this).data('id'));
//     });
//     fetchPlaces({ amenities, states: Object.keys(selectedStates), cities: Object.keys(selectedCities) });
//   });

//   // Event handler for toggling reviews
//   $(document).on('click', '.toggle-reviews', function () {
//     const span = $(this);
//     const placeId = span.data('place-id');
//     const reviewList = span.closest('.reviews').find('.review-list');

//     if (span.text() === 'show') {
//       $.get(`http://0.0.0.0:5001/api/v1/places/${placeId}/reviews`, function (data) {
//         console.log('Fetched reviews:', data); // Log fetched reviews
//         reviewList.empty();
//         if (Array.isArray(data) && data.length > 0) {
//           for (const review of data) {
//             console.log('Appending review:', review); // Log each review being appended
//             reviewList.append(`<li>${review.text}</li>`);
//           }
//         } else {
//           console.log('No reviews found');
//           reviewList.append('<li>No reviews available</li>');
//         }
//         span.text('hide');
//       }).fail(function () {
//         console.error('Failed to fetch reviews');
//       });
//     } else {
//       reviewList.empty();
//       span.text('show');
//     }
//   });
// });
