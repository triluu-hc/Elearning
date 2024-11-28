celery -A elearning worker -l info
celery -A elearning beat -l info
# E-learning Platform

1. Building an E-Learning Platform:
- Course: Represents a course and includes fields like title, description, created_at, and updated_at.
- Module: Each course can contain multiple modules. Fields include title, description, course (foreign key to Course), and order (for ordering modules).
- Content: This will represent diverse types of content that can be added to a module (e.g., text, video, quiz). Create an abstract base class Content and then subclass it to create specific content types, like TextContent and VideoContent.
2. Create REST API Endpoints with Django REST framework
Course API: Create REST API endpoints for managing courses (CRUD operations). Allow users to:
- Create a new course.
- Retrieve course details.
- Update course information.
- Delete a course.
Module and Content API: Implement REST API endpoints for managing modules and associated content within each course.
3. Order Modules and Content
- Implement logic to reorder modules within a course and contents within each module using an integer field order. This will help structure the content display order.
- Create an API endpoint for reordering modules or content using drag-and-drop functionality.
4. Background Tasks with Celery and Redis
- Set up Celery and Redis to handle background tasks in the project.
- Create a Celery task to send an email notification to a user when a new course is created. Configure Redis as the message broker for Celery.
- Implement a scheduled Celery task (run daily) to check for and archive any courses that haven’t been updated in a certain period (e.g., one year).
5. Unit Testing
- Write unit tests for all key components, particularly for: 
+ REST API endpoints (create, retrieve, update, delete).
+ Model methods, especially those involving ordering and relationships.
+ Celery tasks, using mocking to simulate asynchronous task execution.
- Achieve test coverage for all REST API endpoints and Celery tasks.
6. User Authentication and Permissions
- Create views and endpoints for user registration, login, and logout.
- Set up authentication for API endpoints using Django’s built-in authentication system.
- Add permissions to ensure that only authorized users can create, update, or delete courses and modules.
7. Redis Caching
- Configure Redis as a caching backend in Django.
- Cache the results of frequently accessed API calls, such as retrieving course details, to reduce database load.
- Set expiration times for cache entries and implement logic to invalidate the cache when course data is updated.
8. Student Registration and Enrollment
- Implement an API for student registration and allow students to enroll in courses.
- Add endpoints to let students view their enrolled courses.
- Store enrollment data in the database and create an efficient query to fetch courses a student has enrolled in.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the necessary packages

```bash
pip install -r requirements.txt
```

## Usage

These following table shows all the HTTP available endpoints to this project

| Scope | URL |
| ------------- | ------------- |
| Collection of subjects  -> /subjects/  |
| Subject -> /subjects/{id}  |
| Collection of courses -> /courses/ 
| Course -> /courses/{id} |
| Collection of modules -> /modules/ |
| Module -> /modules/{id} |
| Collection of contents -> /contents/ |
| Content -> /contents/{id} |
| Enrollment -> /students/{id}/register
                /students/{id}/enrollment

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)