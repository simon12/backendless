# Round of Drinks Feature Implementation Plan

## Feature Overview
The "Round of Drinks" feature will allow users to share their endpoints with others for a limited time or number of uses, similar to buying a round of drinks for friends.

## Implementation Steps

### 1. Database Model Changes
- Create a new `DrinkRound` model that links to an `Endpoint` and tracks:
  - Creator (user who created the round)
  - Name/description
  - Expiration time
  - Usage limit
  - Access token (for authentication)
  - Created/updated timestamps

### 2. API Endpoints
- Add endpoints for:
  - Creating a new drink round
  - Listing active drink rounds
  - Using a shared endpoint via a drink round
  - Revoking a drink round

### 3. User Interface Changes
- Add a "Share a Round" button to the endpoint detail page
- Create a modal for configuring sharing options
- Add a "My Rounds" section to the dashboard
- Create a landing page for accessing shared endpoints

### 4. Authentication & Security
- Generate secure access tokens for shared endpoints
- Implement rate limiting and usage tracking
- Ensure proper permission checks

### 5. Email/Notification
- Send notification when a round is created
- Optionally notify when a round is used or expires

## Implementation Details

### DrinkRound Model
```python
class DrinkRound(models.Model):
    endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    access_token = models.CharField(max_length=64, unique=True)
    expires_at = models.DateTimeField()
    usage_limit = models.PositiveIntegerField(default=10)
    usage_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Views to Implement
1. `DrinkRoundCreateView` - For creating a new round
2. `DrinkRoundListView` - For listing a user's rounds
3. `DrinkRoundDetailView` - For viewing details of a round
4. `DrinkRoundUseView` - For using a shared endpoint
5. `DrinkRoundRevokeView` - For revoking access to a round

### Templates to Create/Modify
1. `endpoint_detail.html` - Add sharing button
2. `drink_round_create.html` - Form for creating a round
3. `drink_rounds.html` - List of user's rounds
4. `drink_round_detail.html` - Details of a specific round
5. `drink_round_use.html` - Interface for using a shared endpoint

### URL Structure
- `/endpoints/<id>/share/` - Create a new round
- `/rounds/` - List user's rounds
- `/rounds/<id>/` - View round details
- `/rounds/<id>/revoke/` - Revoke a round
- `/shared/<token>/` - Access a shared endpoint

