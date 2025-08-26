# Social Media API - Posts and Comments

## Posts Endpoints

### List Posts
**GET** `/api/posts/`

Retrieve a paginated list of all posts.

Query Parameters:
- `page`: Page number (default: 1)
- `search`: Search in title and content
- `author`: Filter by author ID

Example Response:
```json
{
  "count": 23,
  "next": "http://example.com/api/posts/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "author": 1,
      "author_username": "username",
      "title": "Post title",
      "created_at": "2025-08-26T10:00:00Z",
      "comments_count": 5
    },
    ...
  ]
}
```

### Create Post
**POST** `/api/posts/`

Authentication required. Creates a new post.

Request Body:
```json
{
  "title": "New Post Title",
  "content": "This is the content of my new post."
}
```

### Retrieve Post
**GET** `/api/posts/{id}/`

Retrieve a specific post by ID, including its comments.

Example Response:
```json
{
  "id": 1,
  "author": 1,
  "author_username": "username",
  "title": "Post title",
  "content": "Post content here...",
  "created_at": "2025-08-26T10:00:00Z",
  "updated_at": "2025-08-26T10:00:00Z",
  "comments": [
    {
      "id": 1,
      "post": 1,
      "author": 2,
      "author_username": "commenter",
      "content": "Great post!",
      "created_at": "2025-08-26T11:00:00Z",
      "updated_at": "2025-08-26T11:00:00Z"
    }
  ],
  "comments_count": 1
}
```

### Update Post
**PUT/PATCH** `/api/posts/{id}/`

Authentication required. User can only update their own posts.

Request Body (PUT):
```json
{
  "title": "Updated Title",
  "content": "Updated content here..."
}
```

Request Body (PATCH):
```json
{
  "title": "Updated Title"
}
```

### Delete Post
**DELETE** `/api/posts/{id}/`

Authentication required. User can only delete their own posts.

## Comments Endpoints

### List Comments
**GET** `/api/comments/`

Retrieve a paginated list of all comments.

Query Parameters:
- `page`: Page number (default: 1)
- `post`: Filter by post ID
- `author`: Filter by author ID

Example Response:
```json
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "post": 1,
      "author": 2,
      "author_username": "commenter",
      "content": "Great post!",
      "created_at": "2025-08-26T11:00:00Z",
      "updated_at": "2025-08-26T11:00:00Z"
    },
    ...
  ]
}
```

### Create Comment
**POST** `/api/comments/`

Authentication required. Creates a new comment.

Request Body:
```json
{
  "post": 1,
  "content": "This is my comment on the post."
}
```

### Retrieve Comment
**GET** `/api/comments/{id}/`

Retrieve a specific comment by ID.

### Update Comment
**PUT/PATCH** `/api/comments/{id}/`

Authentication required. User can only update their own comments.

Request Body (PATCH):
```json
{
  "content": "Updated comment content"
}
```

### Delete Comment
**DELETE** `/api/comments/{id}/`

Authentication required. User can only delete their own comments.

## Authentication

All endpoints that modify data (POST, PUT, PATCH, DELETE) require authentication.
Include the authentication token in the request header:

```
Authorization: Token <your_token>
```

You can obtain a token by registering or logging in through the accounts API.
