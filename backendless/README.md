# Backendless

A Django-based platform for creating AI-powered APIs without writing backend code.

## Round of Drinks Feature

The "Round of Drinks" feature allows users to share their endpoints with others for a limited time or number of uses, similar to buying a round of drinks for friends.

### Key Features

- **Share Endpoints**: Users can share their endpoints with others without giving them full access to their account
- **Time-Limited Access**: Shared endpoints automatically expire after a configurable time period
- **Usage Limits**: Set a maximum number of times the shared endpoint can be used
- **Revocation**: Ability to revoke access at any time
- **Tracking**: Monitor usage of shared endpoints

### How It Works

1. **Create a Round**: From any endpoint, click "Share a Round" to create a new drink round
2. **Configure Sharing**: Set a name, description, expiration time, and usage limit
3. **Share the Link**: Copy and share the generated link with others
4. **Monitor Usage**: Track how many times your shared endpoint has been used
5. **Revoke Access**: Revoke access at any time if needed

### Technical Implementation

- **DrinkRound Model**: Stores sharing configuration and tracks usage
- **Access Tokens**: Secure, unique tokens for accessing shared endpoints
- **Expiration Logic**: Automatic expiration based on time or usage
- **API Integration**: Shared endpoints use the owner's API key behind the scenes

### Use Cases

- **Client Demos**: Share a demo of your endpoint with potential clients
- **Temporary Collaborations**: Give temporary access to collaborators
- **Limited Trials**: Offer limited trials of your endpoints to others
- **Event-Based Access**: Provide access during specific events or timeframes

