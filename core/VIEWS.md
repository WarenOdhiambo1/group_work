# Core Views Documentation

## Overview
This module contains the core views for the Backyard Adventures application.

## Views

### `home(request)`
**Purpose:** Renders the home page with a gallery of activities.

**Parameters:**
- `request`: Django HttpRequest object

**Returns:**
- Rendered template `home.html` with context containing up to 6 activities

**Template Context:**
- `activities`: QuerySet of Activity objects (limited to 6)

---

### `create_admin(request)`
**Purpose:** Programmatically creates a superuser account for administrative access.

**Parameters:**
- `request`: Django HttpRequest object

**Returns:**
- HttpResponse with success message if admin created
- HttpResponse with info message if admin already exists

**Credentials:**
- Username: `admin`
- Email: `admin@ba.com`
- Password: `password123`

**Note:** This view checks for existing admin to prevent duplicate creation errors.
