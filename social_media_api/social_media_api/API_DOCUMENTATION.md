# Social Media API Documentation

## Likes and Notifications

### Like Endpoints

#### Like a Post
- **URL**: `/api/posts/{post_id}/like/`
- **Method**: POST
- **Auth Required**: Yes
- **Description**: Like a specific post. Creates a notification for the post author.
- **Success Response**:
  - Code: 200
  - Content: `{"detail": "Post liked successfully."}`
- **Error Response**:
  - Code: 400
  - Content: `{"detail": "You have already liked this post."}`

#### Unlike a Post
- **URL**: `/api/posts/{post_id}/unlike/`
- **Method**: POST
- **Auth Required**: Yes
- **Description**: Unlike a previously liked post.
- **Success Response**:
  - Code: 200
  - Content: `{"detail": "Post unliked successfully."}`
- **Error Response**:
  - Code: 400
  - Content: `{"detail": "You have not liked this post."}`

### Notification Endpoints

#### List Notifications
- **URL**: `/api/notifications/`
- **Method**: GET
- **Auth Required**: Yes
- **Description**: Retrieve list of notifications for the authenticated user.
- **Success Response**:
  - Code: 200
  - Content: Array of notifications
  ```json
  [
    {
      "id": 1,
      "actor": "username",
      "verb": "liked",
      "target": "Post object",
      "is_read": false,
      "timestamp": "2025-08-26T10:00:00Z"
    }
  ]
  ```

#### Mark Notification as Read
- **URL**: `/api/notifications/{notification_id}/mark_as_read/`
- **Method**: POST
- **Auth Required**: Yes
- **Description**: Mark a specific notification as read.
- **Success Response**:
  - Code: 200
  - Content: `{"status": "notification marked as read"}`

### Notification Types

The system generates notifications for the following actions:
1. When a user likes your post
2. When a user comments on your post
3. When a user starts following you

### Example Usage

1. Liking a Post:
```bash
curl -X POST \
  -H "Authorization: Token YOUR_AUTH_TOKEN" \
  http://api/posts/1/like/
```

2. Getting Notifications:
```bash
curl -H "Authorization: Token YOUR_AUTH_TOKEN" \
  http://api/notifications/
```
