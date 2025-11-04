# Databases2024

## Overview
This project is a database-driven web application built with **Flask**, featuring functionality for both airline staff and customers.  
Users can create flights, manage bookings, view reports, and leave reviews.

---

## File Descriptions

### SQL Files (`/sql`)
| File | Description |
|------|--------------|
| `inserts.sql` | Sample data to test features and populate the database. |
| `tables.sql` | SQL schema defining all database tables. |

---

### Static Files (`/static/css`)
| File | Description |
|------|--------------|
| `main.css` | Contains all styling for the web interface. |

---

### Templates (`/templates`)
| File | Description |
|------|--------------|
| `base.html` | Base layout with navigation bar; extended by all other templates. |
| `home.html` | Home page with flight search for both guests and logged-in users. |
| `login.html` | Login selection page for customer or staff. |
| `login_customer.html` | Customer login page (uses customer email). |
| `login_staff.html` | Airline staff login page (uses staff username). |
| `register.html` | Registration selection page for customer or staff. |
| `register_customer.html` | Registration form for new customers. |
| `register_staff.html` | Registration form for airline staff. |
| `customer_dashboard.html` | Dashboard for customers: view/search purchased flights. |
| `staff_dashboard.html` | Dashboard for airline staff: access flight management features. |
| `create_flight.html` | Form for airline staff to create new flights. |
| `update_flight_status.html` | Form for staff to update flight statuses. |
| `staff_view_flights.html` | Airline staff view of all flights. |
| `staff_flight_customers.html` | Displays customers for a specific flight. |
| `staff_view_reviews.html` | Shows customer average ratings for a flight. |
| `staff_view_reports.html` | Displays ticket sales and revenue reports by airline. |
| `add_airplane.html` | Form to add airplanes. |
| `add_airport.html` | Form to add airports. |
| `cancel_trip.html` | Page for customers to cancel booked flights. |
| `purchase_ticket.html` | Form for customers to purchase tickets. |
| `review_flight.html` | Page for customers to review completed flights. |
| `view_comments.html` | Page for airline staff to view customer comments. |
| `search_results.html` | Displays search results for flights. |

---

### Application Logic
| File | Description |
|------|--------------|
| `app.py` | Main Flask application with all backend logic and routes. |

---

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Databases2024.git
   cd Databases2024
