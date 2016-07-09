# Introduction
### Clean API Responses
# Auth

### Sign In
**URL**: `/api/auth/actions/make-token/`. Endpoint to provide access tokens to authentication flow.

### Refresh Access Token
**URL**: POST `/api/auth/actions/refresh-token/`. Endpoint to provide access token to Refresh token flow

### Revoke Access Token
**URL**: POST `/api/auth/actions/revoke-token/`. Endpoint to provide access token to Revoke token flow

### Convert Access Token
**URL**: POST `/api/auth/actions/convert-token/`. Endpoint to convert Social Acces Token for Django Acces Token

### Reset Password
**URL**: POST `/api/auth/actions/reset-password/`. Send password reset token to user by username or email

### Confirm Reset Password
**URL**: POST `/api/auth/actions/confirm-reset-password/`. Reset password from password reset token

### Check Email
**URL**: POST `/api/auth/actions/check-email/`. Check if an email is available

### Check Username
**URL**: POST `/api/auth/actions/check-username/`. Check if an username is available

### Register
**URL**: POST `/api/auth/register/`. Register a new user

### Send confirmation
**URL**: POST `/api/auth/register/actions/send-confirmation/`. Send account confirmation to an inactive user by email or username

### Confirm Account
**URL**: POST `/api/auth/register/actions/confirm/`. Activate an user account by confirmation token




# Account
### Get Profile
