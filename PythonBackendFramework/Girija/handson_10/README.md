# Task 1: Decompose the Monolith into Services

| Service | Responsibility | Endpoints | Database |
|----------|---------------|-----------|----------|
| Course Service | Course & Department CRUD | /api/courses | course.db |
| Student Service | Student CRUD & Enrollment | /api/students | student.db |
| Auth Service | Registration, Login, JWT | /api/auth | auth.db |
| Notification Service | Email Notifications | /api/notifications | notification.db |

# Task 2: Inter-Service Communication and API Gateway Pattern

Synchronous (HTTP)
- Immediate response
- Easy implementation
- Services tightly coupled
- Failure propagates

Asynchronous (RabbitMQ/Kafka)
- Loosely coupled
- Better scalability
- Eventual consistency
- Suitable for notifications, logging, analytics and background jobs