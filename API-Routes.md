User Routes
GET /users: Retrieve all users
GET /users/<user_id>: Retrieve a specific user by ID
POST /users: Create a new user
PUT /users/<user_id>: Update a specific user by ID
DELETE /users/<user_id>: Delete a specific user by ID

Address Routes
GET /addresses: Retrieve all addresses
GET /addresses/<address_id>: Retrieve a specific address by ID
POST /addresses: Create a new address
PUT /addresses/<address_id>: Update a specific address by ID
DELETE /addresses/<address_id>: Delete a specific address by ID

*Order Routes
GET /orders: Retrieve all orders
GET /orders/<order_id>: Retrieve a specific order by ID
POST /orders: Create a new order
PUT /orders/<order_id>: Update a specific order by ID
DELETE /orders/<order_id>: Delete a specific order by ID

Doctor Routes
GET /doctors: Retrieve all doctors
GET /doctors/<doctor_id>: Retrieve a specific doctor by ID
POST /doctors: Create a new doctor
PUT /doctors/<doctor_id>: Update a specific doctor by ID
DELETE /doctors/<doctor_id>: Delete a specific doctor by ID
Comment Routes
GET /comments: Retrieve all comments
GET /comments/<comment_id>: Retrieve a specific comment by ID
POST /comments: Create a new comment
PUT /comments/<comment_id>: Update a specific comment by ID
DELETE /comments/<comment_id>: Delete a specific comment by ID
Category Routes
GET /categories: Retrieve all categories
GET /categories/<category_id>: Retrieve a specific category by ID
POST /categories: Create a new category
PUT /categories/<category_id>: Update a specific category by ID
DELETE /categories/<category_id>: Delete a specific category by ID
Product Categories Routes
GET /product_categories: Retrieve all product categories
GET /product_categories/<product_id>: Retrieve product categories by product ID
POST /product_categories: Create a new product category
DELETE /product_categories/<product_id>/<category_id>: Delete a product category by product ID and category ID
Prescription Routes
GET /prescriptions: Retrieve all prescriptions
GET /prescriptions/<prescription_id>: Retrieve a specific prescription by ID
POST /prescriptions: Create a new prescription
DELETE /prescriptions/<prescription_id>: Delete a specific prescription by ID
Product Routes
GET /products: Retrieve all products
GET /products/<product_id>: Retrieve a specific product by ID
POST /products: Create a new product
PUT /products/<product_id>: Update a specific product by ID
DELETE /products/<product_id>: Delete a specific product by ID
Product Tags Routes
GET /product_tags: Retrieve all product tags
GET /product_tags/<product_id>: Retrieve product tags by product ID
POST /product_tags: Create a new product tag
DELETE /product_tags/<product_id>/<tag_id>: Delete a product tag by product ID and tag ID
Product Images Routes
GET /product_images: Retrieve all product images
GET /product_images/<product_id>: Retrieve product images by product ID
POST /product_images: Create a new product image
DELETE /product_images/<image_id>: Delete a specific product image by ID
Shipping Methods Routes
GET /shipping_methods: Retrieve all shipping methods
GET /shipping_methods/<method_id>: Retrieve a specific shipping method by ID
POST /shipping_methods: Create a new shipping method
PUT /shipping_methods/<method_id>: Update a specific shipping method by ID
DELETE /shipping_methods/<method_id>: Delete a specific shipping method by ID
Shipping Information Routes
GET /shipping_information: Retrieve all shipping information
GET /shipping_information/<info_id>: Retrieve specific shipping information by ID
POST /shipping_information: Create new shipping information
PUT /shipping_information/<info_id>: Update specific shipping information by ID
DELETE /shipping_information/<info_id>: Delete specific shipping information by ID
Roles Routes
GET /roles: Retrieve all roles
GET /roles/<int:role_id>: Retrieve a specific role by ID
POST /roles: Create a new role
PUT /roles/<int:role_id>: Update a specific role by ID
DELETE /roles/<int:role_id>: Delete a specific role by ID
Reviews Routes
GET /reviews: Retrieve all reviews
GET /reviews/<review_id>: Retrieve a specific review by ID
POST /reviews: Create a new review
PUT /reviews/<review_id>: Update a specific review by ID
DELETE /reviews/<review_id>: Delete a specific review by ID
Miscellaneous Routes
GET /api/v1/status: Check the status of the API
GET /: Home route
GET /jopmed-home: Home route