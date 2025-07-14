# Grocery Store Shopping Cart Application

A modern, full-stack grocery shopping cart application built with Flask and SQLite. Features a beautiful, responsive frontend with glassmorphism design and a comprehensive database administration interface.

## Features

### Customer Interface
- **Modern UI Design**: Glassmorphism effects, gradients, and smooth animations
- **Product Catalog**: Browse products by category with search functionality
- **Shopping Cart**: Add, update, and remove items with real-time updates
- **Checkout System**: Complete orders with customer information
- **Real-time Updates**: Cart summary updates instantly
- **Responsive Design**: Works seamlessly on desktop and mobile devices

### Admin Interface
- **Database Administration**: View all database tables in a user-friendly interface
- **Real-time Statistics**: Live dashboard showing product count, cart items, orders, and order items
- **Data Visualization**: Color-coded data types and formatted displays
- **Auto-refresh**: Tables update automatically every 30 seconds
- **Modern Admin Panel**: Clean, professional interface for data management

### Technical Features
- **SQLite Database**: Lightweight, file-based database
- **RESTful API**: Clean API endpoints for all operations
- **Stock Management**: Automatic inventory tracking
- **Order Management**: Complete order processing workflow
- **Error Handling**: Comprehensive error handling and user feedback

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Modern CSS with glassmorphism effects
- **Icons**: Unicode emojis and symbols

## Project Structure

```
grocery-store-app/
├── app.py                 # Main Flask application
├── grocery_store.db      # SQLite database (created automatically)
├── templates/
│   ├── index.html        # Customer shopping interface
│   └── admin.html        # Database administration interface
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── README.md
```

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the project files**
   ```bash
   mkdir grocery-store-app
   cd grocery-store-app
   ```

2. **Install Flask**
   ```bash
   pip install flask
   ```

3. **Create the templates directory**
   ```bash
   mkdir templates
   ```

4. **Add the HTML files**
   - Save the first HTML content as `templates/index.html`
   - Save the second HTML content as `templates/admin.html`

5. **Add the Flask application**
   - Save the Python code as `app.py`

6. **Run the application**
   ```bash
   python app.py
   ```

## Usage

### Starting the Application

1. Run the Flask application:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   - **Shopping Interface**: `http://localhost:5000`
   - **Admin Interface**: `http://localhost:5000/admin`

### Customer Shopping Flow

1. **Browse Products**: View all available products with categories, prices, and stock levels
2. **Search & Filter**: Use the search box or category filter to find specific items
3. **Add to Cart**: Click "Add to Cart" on any product (disabled for out-of-stock items)
4. **View Cart**: Click the cart summary in the header to open the cart modal
5. **Update Quantities**: Use +/- buttons or type quantities directly
6. **Checkout**: Enter your name (optional) and click "Checkout"
7. **Order Confirmation**: Receive order confirmation with order ID

### Admin Functions

1. **View Database Tables**: Access comprehensive views of all database tables
2. **Monitor Statistics**: Real-time dashboard showing key metrics
3. **Data Management**: View products, cart items, orders, and order items
4. **Auto-refresh**: Tables automatically update every 30 seconds

## Database Schema

### Products Table
- `id`: Primary key
- `name`: Product name
- `category`: Product category
- `price`: Product price
- `stock`: Available quantity
- `image_url`: Product image URL

### Cart Table
- `id`: Primary key
- `product_id`: Foreign key to products
- `quantity`: Number of items
- `added_date`: When item was added

### Orders Table
- `id`: Primary key
- `customer_name`: Customer name
- `total_amount`: Order total
- `order_date`: When order was placed
- `status`: Order status

### Order Items Table
- `id`: Primary key
- `order_id`: Foreign key to orders
- `product_id`: Foreign key to products
- `quantity`: Number of items ordered
- `price`: Price at time of order

## API Endpoints

### Product Endpoints
- `GET /api/products` - Get all products
- `GET /` - Customer shopping interface

### Cart Endpoints
- `GET /api/cart` - Get cart items
- `POST /api/cart/add` - Add item to cart
- `POST /api/cart/update` - Update cart item quantity
- `POST /api/cart/clear` - Clear entire cart

### Order Endpoints
- `POST /api/checkout` - Process checkout and create order

### Admin Endpoints
- `GET /admin` - Admin dashboard interface
- `GET /api/admin/tables` - Get all database tables data

## Sample Data

The application comes with pre-populated sample data including:
- 12 sample products across categories (Fruits, Dairy, Bakery, Meat, Grains, Vegetables, Beverages)
- Realistic pricing and stock levels
- Product categories for easy browsing

## Customization

### Adding New Products
Products can be added directly to the database or by modifying the sample data in `app.py`.

### Styling Customization
The application uses modern CSS with:
- CSS Grid for responsive layouts
- Flexbox for component alignment
- CSS gradients for visual appeal
- Custom animations and transitions
- Glassmorphism effects with backdrop-filter

### Adding New Features
The modular structure makes it easy to add:
- User authentication
- Product images
- Order tracking
- Inventory management
- Payment processing

## Security Considerations

**Note**: This is a demonstration application. For production use, implement:
- Input validation and sanitization
- SQL injection protection
- User authentication
- Session management
- HTTPS encryption
- Rate limiting

## Troubleshooting

### Common Issues

1. **Database not found**: The database is created automatically on first run
2. **Templates not found**: Ensure `templates/` directory exists with HTML files
3. **Port already in use**: Change port in `app.py` or stop other Flask applications
4. **Import errors**: Ensure Flask is installed (`pip install flask`)
