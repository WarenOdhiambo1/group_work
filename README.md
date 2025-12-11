# 🌊 Backyard Adventures - Booking System

Modern, responsive booking and inquiry management system for water sports rentals and guided tours in Jacksonville, Florida.



---

## ✨ Features

 Customer-Facing Features
- ✅ **Modern UI/UX**: Light-green color scheme, Nunito font, mobile-responsive
- ✅ **Booking System**: Conflict-free reservations with automatic validation
- ✅ **Contact/Inquiry Form**: Direct communication with staff (auto-assigned to Melissa)
- ✅ **Activities Gallery**: Pinterest-integrated photo gallery with working links
- ✅ **Responsive Design**: Perfect on mobile, tablet, and desktop
- ✅ **Mobile Navigation**: Hamburger menu with smooth transitions

 Admin Features
- ✅ **Activity Management**: Add/edit tours and rentals with pricing
- ✅ **Booking Dashboard**: View, filter, and confirm reservations
- ✅ **Inquiry Management**: Track customer inquiries with status updates
- ✅ **Staff Management**: Add users like Melissa with role-based access
- ✅ **Conflict Prevention**: Automatic detection of double-bookings
- ✅ **Daily Reports**: Filter bookings by date for morning reports

---

Business Context

**Company**: Backyard Adventures  
**Location**: Jacksonville, Florida  
**Owners**: Shawn & Harry Weaver (brothers)  
**Staff**: Melissa Smith (receptionist)  

**Services**:
-  Equipment Rentals (kayaks, paddleboards)
-  Guided Water Tours

**Problem Solved**: Replaced manual "binder" booking system with digital solution that prevents scheduling conflicts and provides business analytics.

---

 Technical Stack

- **Backend**: Django 6.0 (Python 3.12+)
- **Database**: SQLite3 (development), PostgreSQL-ready
- **Frontend**: Django Templates + Custom CSS
- **Font**: Nunito (Google Fonts)
- **Color Scheme**: Light Green (#7EC850) - nature-inspired
- **Deployment**: Gunicorn + WhiteNoise (static files)

---

Installation & Setup

### Prerequisites
- Python 3.12+
- pip
- Git

### Quick Start
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Apply database migrations
python manage.py makemigrations
python manage.py migrate

# 3. Create admin user
python manage.py createsuperuser

# 4. Run development server
python manage.py runserver

# 5. Access application
# Home: http://localhost:8000/
# Admin: http://localhost:8000/admin/
```

---




### Via Admin Panel
1. Go to `/admin/`
2. Navigate to **Staff Profiles**
3. Click **Add Staff Profile**
4. Select existing user or create new one
5. Set role to **Receptionist**
6. Check **Can receive inquiries**
7. Save

---

## 📊 Database Models

### 1. Activity
Tours and rental equipment inventory
- Name, Type (TOUR/RENTAL), Price, Description
- Image URL (Pinterest/external links)

### 2. Booking
Customer reservations with conflict prevention
- Customer details (name, email, phone)
- Activity, Date, Time, Number of guests
- Confirmation status, Notes
- **Auto-conflict detection**: Prevents double-booking

### 3. Inquiry
Customer contact/inquiry system
- Name, Email, Phone, Subject, Message
- Status (NEW/IN_PROGRESS/RESOLVED)
- **Auto-assignment**: Routes to receptionist (Melissa)

### 4. StaffProfile
Staff member roles and permissions
- User (Django User model extension)
- Role (RECEPTIONIST/TOUR_GUIDE/MANAGER/ADMIN)
- Inquiry routing control

---

## 🎨 Design System

### Color Palette
```css
--primary-green: #7EC850;    /* Main brand color */
--light-green: #A8E67D;      /* Accents */
--dark-green: #5BA032;       /* Hover states */
--accent-green: #E8F5E0;     /* Backgrounds */
--text-dark: #2C3E2E;        /* Primary text */
--text-light: #6B8068;       /* Secondary text */
```

### Typography
Font**: Nunito (300, 400, 600, 700, 800 weights)
Base Size**: 14px
Small Fonts

### Responsive Breakpoints
- **Mobile**: 320px - 767px
- **Tablet**: 768px - 1024px
- **Desktop**: 1025px+

---

## 🔐 Admin Panel Guide

### Accessing Admin
1. Navigate to `/admin/`
2. Login with superuser credentials
3. Dashboard shows all manageable sections

### Admin Sections

#### 1. Activities
- Add new tours/rentals
- Set pricing and descriptions
- Add Pinterest image URLs

#### 2. Bookings
- View all reservations
- Filter by date, activity, status
- Quick confirm/reject bookings
- **Morning Report**: Filter by today's date

#### 3. Inquiries
- View customer messages
- Assign to staff members
- Update status (NEW → IN_PROGRESS → RESOLVED)
- **Auto-assignment**: New inquiries go to Melissa

#### 4. Staff Profiles
- Add staff members (like Melissa)
- Set roles and permissions
- Control inquiry routing

---

## 📸 Pinterest Gallery Integration



### How It Works
- Pinterest images are loaded via direct image URLs
- Gallery links use `target="_blank"` for new tab opening
- Hover effects show overlay with activity name
- Responsive masonry grid layout

---

## 🧪 Testing Checklist

### Booking System
- [ ] Create new booking (should succeed)
- [ ] Try to book same activity on same date (should fail with conflict message)
- [ ] Edit existing booking
- [ ] Confirm booking via admin panel
- [ ] View daily report in admin

### Inquiry System
- [ ] Submit contact form
- [ ] Check admin - inquiry should be auto-assigned to Melissa
- [ ] Update inquiry status (NEW → IN_PROGRESS → RESOLVED)

### UI/UX
- [ ] Test mobile responsive design (hamburger menu)
- [ ] Click all Pinterest gallery links (should open in new tab)
- [ ] Test all navigation links
- [ ] Check form validation (empty fields should show errors)
- [ ] Verify success/error messages display correctly

---



---

## 🚀 Deployment

### Production Checklist
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SECRET_KEY = os.environ.get('SECRET_KEY')

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Deployment Commands
```bash
# Collect static files
python manage.py collectstatic --noinput

# Apply migrations
python manage.py migrate

# Start Gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```



## 🎯 Key Business Benefits

1. **Conflict Prevention**: No more double-bookings
2. **Automated Routing**: Inquiries auto-assigned to Melissa
3. **Mobile Access**: Book from anywhere, any device
4. **Analytics Ready**: Data structured for future reporting
5. **Professional Image**: Modern, branded website
6. **Time Savings**: Replaces manual binder system

---

Support

### For Admin/Staff
<!-- - **Melissa** (Receptionist): Handles inquiries and bookings
- **Admin Panel**: `/admin/` for all management tasks -->

### For Developers
- See `DEVELOPMENT.md` for technical details
- Django documentation: https://docs.djangoproject.com/

### For Business Owners (Shawn & Harry)
- Dashboard: `/dashboard/` (analytics)
- Reports: Available in admin panel

---



### Version 2.0 (Current)
✅ Modern light-green UI with Nunito font  
✅ Small font sizes for clean, modern look  
✅ Mobile-responsive navigation with hamburger menu  
✅ Pinterest gallery with working external links  
✅ Staff profile system (Melissa as receptionist)  
✅ Auto-inquiry assignment to staff  
✅ Enhanced booking form (phone, time, guests, notes)  
✅ Comprehensive admin panel customizations  

---

## 📄 License

Proprietary software for Backyard Adventures, Jacksonville, Florida.

---





**Last Updated**: 2024-12-11  
**Version**: 2.0  
**Django**: 6.0  
**Python**: 3.12+
