# Databases2024
file_desc.md

 File List + Descriptions
 This file (file_desc.md) serves as a brief overview of what files are in the project and what each of them do.
 sql/
 inserts.sql: Sample data to test features and populate the database
 tables.sql: SQL schema for all tables in the project
 static/css/
 main.css: CSS file that contains all the styling for the site
 templates/
 add_airplane.html: Page for airline staff to add an airplane.
 add_airport.html: Page for airline staff to add an airport.
 base.html: Base template for other HTML to extend from. Contains the nav bar.
 create_flight.html: Page for airline staff to create a new flight
 customer_dashboard.html: Dashboard for customers. Contains flight search and customer's
 purchased flights.
 home.html: Home page. Allows logged out and logged in users to search flights.
 login.html: Login selection page. Can choose to login as staff or customer.
 login_customer.html: Customer login page (uses customer email).
 login_staff.html: Airline staff login page (uses staff username).
 purchase_ticket.html: Page that contains a form to purchase flight tickets for customers.
 register.html: Landing page for user registration. Provides options between customer and
 staff.
 register_customer.html: Page that contains a registration form for new customers.
 register_staff.html: Page that contains a registration form for airline staff members.
 search_results.html: Page that displays flight search search_results.
 staff_dashboard.html: Dashboard for airline staff. Contains buttons that lead to other use
 cases.
 staff_flight_customers.html: Shows the customers of a flight.
 staff_view_flights.html: Airline staff view of all flights.
 update_flight_status.html: Page that contains the form for staff to update flight status.
 staff_view_reviews.html: Page for staff to view customer average ratings for a specific flight.
 staff_view_reports.html: Page for staff to view the number of tickets sold and total revenue
 for all the flights within a specific airline
 view_comments.html: Page for airline staff to view comments/reviews for a specific flight.
 cancel_trip.html: Page for customers to cancel a specific flight that they booked.
 review_flight.html: Page to collect customer feedback for a specific flight (Rating and
 comments).
 app.py: Main flask application with all the backend logic and routes
 1 / 1
