# NutriPlan - Your Personal Nutrition Tracker

## Project Overview

**NutriPlan** is a Django-based web application designed to help users track their nutrition and improve their eating habits. The platform allows users to create personalized meal plans, track their progress, and purchase tailored plans from certified nutritionists. This project was developed as part of the Software Engineering course and is designed to provide an intuitive and accessible solution for managing dietary needs.

## Features

1. **User Registration and Authentication**:
   - Users can sign up as regular users or nutritionists. They will receive an email confirmation to verify their account.
   - Password recovery functionality is available, allowing users to reset their passwords through an email verification system.

2. **Meal Plan Creation**:
   - Users can create their own meal plans, adding meals for specific days and times.
   - Nutritionists can create public meal plans, which are visible to all users and can be purchased.

3. **Meal Tracking and Notifications**:
   - Users receive notifications an hour before each scheduled meal.
   - Users can track their progress by checking off meals and monitoring their adherence to the plan.

4. **User Types**:
   - **Regular Users**: Can create their own meal plans, track progress, and leave reviews and ratings for nutritionists and their plans.
   - **Nutritionists**: Can create and sell meal plans, in addition to the features available to regular users.
   - **Moderators**: Can manage user behavior by deleting inappropriate comments and suspending users.
   - **Administrators**: Can manage the platform, including adding new foods, managing tags, and controlling user privileges.

5. **Search and Review**:
   - Users can search for nutritionists and meal plans using various filters.
   - Users can leave ratings and comments on nutritionists' profiles and their meal plans.

6. **Plan Ordering**:
   - Users can order custom meal plans from nutritionists based on their preferences. They can communicate with the nutritionist through a custom form, and the nutritionist can create a personalized plan for them.

## Technologies Used

- **Django Framework**: The server-side logic is built using Django, providing a robust and scalable backend.
- **MySQL**: The application communicates with a MySQL database to store user information, meal plans, and progress data.
- **Selenium**: Used for testing and automating the browser interactions to ensure the system functions as expected.

## Functional Requirements

- **User Registration and Login**: Users can create an account, log in, and log out. Password recovery via email is also available.
- **Meal Plan Management**: Users can create, delete, and view meal plans. Nutritionists can publish meal plans for others to view and purchase.
- **Progress Tracking**: Users can check off meals they have eaten and track their adherence to the meal plan.
- **Commenting and Rating**: Users can comment on nutritionists and rate their meal plans, which helps others in selecting a suitable plan.
- **Search and Filter**: Users can search for nutritionists and meal plans based on ratings, keywords, or other criteria.

## How to Run

1. **Clone the repository**:

    ```bash
    git clone https://github.com/your-username/nutriplan.git
    ```

2. **Set up the virtual environment**:

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate
    ```

3. **Install the required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```


## Future Improvements

- Add more advanced meal plan customization options.
- Implement push notifications for upcoming meals.
- Enhance the user interface for a better experience on mobile devices.
- Add more detailed analytics and progress tracking for users.

## Conclusion

**NutriPlan** provides a comprehensive solution for tracking and managing nutrition. It allows users to create meal plans, track their progress, and order personalized plans from certified nutritionists. With a combination of Django for the backend and Selenium for testing, this application offers a stable and scalable platform for improving dietary habits.
