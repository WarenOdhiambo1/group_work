# Backyard Adventures - Development Documentation

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Technical Stack](#technical-stack)
3. [Architecture](#architecture)
4. [Database Models](#database-models)
5. [Features](#features)
6. [UI/UX Design](#uiux-design)
7. [Setup & Installation](#setup--installation)
8. [Admin Panel](#admin-panel)
9. [API Endpoints](#api-endpoints)
10. [Testing](#testing)
11. [Deployment](#deployment)

---

## 🎯 Project Overview

**Backyard Adventures** is a comprehensive booking and inquiry management system for a guided tour and water sports rental company in Jacksonville, Florida. The system replaces manual "binder" booking methods with a modern, conflict-free digital solution.

### Business Requirements
- **Owners**: Shawn and Harry Weaver (brothers)
- **Staff**: Melissa Smith (receptionist handling inquiries and reservations)
- **Services**: 
  - Guided water tours
  - Equipment rentals (kayaks, paddleboards)
- **Problem Solved**: Booking conflicts, manual tracking, limited analytics

---

## 🛠 Technical Stack

### Backend
- **Framework**: Django 6.0
- **Language**: Python 3.12+
- **Database**: SQLite3 (development), PostgreSQL (production-ready)
- **Server**: Gunicorn (production)
- **Static Files**: WhiteNoise

### Frontend
- **Template Engine**: Django Templates
- **Styling**: Custom CSS with CSS Grid & Flexbox
- **Font**: Nunito (Google Fonts)
- **Color Scheme**: Light green (#7EC850) - eco-friendly, nature-oriented
- **Responsive**: Mobile-first design approach
- **JavaScript**: Vanilla JS (minimal, progressive enhancement)

### Dependencies
```txt
django==6.0
pandas==2.2.3
matplotlib==3.10.3
gunicorn==23.0.0
psycopg2-binary==2.9.11
whitenoise==6.11.0
```

---

## 🏗 Architecture

### Django Apps Structure
```
webapp/
├── config/              # Project settings & main URLs
│   ├── settings.py      # Django configuration
│   ├── urls.py          # Main URL routing
│   └── wsgi.py          # WSGI application
├── core/                # Core functionality
│   ├── views.py         # Home page, admin creation
│   └── models.py        # (Empty - no models needed)
├── operations/          # Booking & inquiry management
│   ├── models.py        # Activity, Booking, Inquiry, StaffProfile
│   ├── views.py         # Booking, contact, activities views
│   ├── forms.py         # BookingForm, InquiryForm
│   ├── admin.py         # Admin interface customizations
│   └── urls.py          # Operations app URLs
├── analytics/           # Business analytics & dashboard
│   ├── views.py         # Dashboard, reports
│   └── urls.py          # Analytics URLs
├── templates/           # HTML templates
│   ├── base.html        # Base template with navigation
│   ├── home.html        # Landing page
│   └── operations/      # Operations app templates
│       ├── book.html    # Booking form
│       ├── contact.html # Contact/inquiry form
│       └── activities.html # Activities gallery
└── static/              # Static files (CSS, JS, images)
```

### Design Pattern: MTV (Model-Template-View)
Django's MTV pattern separates concerns:
- **Models**: Data structure and business logic
- **Templates**: Presentation layer (HTML)
- **Views**: Request handling and logic

---

## 📊 Database Models

### 1. Activity Model
**Purpose**: Inventory of tours and rentals

```python
class Activity(models.Model):
    ACTIVITY_TYPES = (
        ('TOUR', 'Guided Tour'),
        ('RENTAL', 'Equipment Rental')
    )
    
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=ACTIVITY_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image_url = models.URLField(max_length=500, blank=True)
```

**Fields Explained**:
- `name`: Activity name (e.g., "River Kayaking Tour")
- `type`: TOUR or RENTAL
- `price`: Cost per person/rental
- `description`: Detailed activity description
- `image_url`: External image link (Pinterest, Unsplash, etc.)

---

### 2. Booking Model
**Purpose**: Customer reservations (replaces "binder" system)

```python
class Booking(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20, blank=True, default='')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    guests = models.IntegerField(default=1)
    is_confirmed = models.BooleanField(default=False)
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
```

**Key Features**:
- **Conflict Prevention**: `clean()` method validates no double-booking
- **Confirmation System**: `is_confirmed` tracks booking status
- **Audit Trail**: `created_at` timestamp

**Conflict Detection Logic**:
```python
def clean(self):
    existing_bookings = Booking.objects.filter(
        activity=self.activity, 
        date=self.date,
        is_confirmed=True
    )
    if self.pk:
        existing_bookings = existing_bookings.exclude(pk=self.pk)
    
    if existing_bookings.exists():
        raise ValidationError(f"Conflict! {self.activity.name} is already booked on {self.date}.")
```

---

### 3. Inquiry Model
**Purpose**: Customer contact/inquiry system for Melissa

```python
class Inquiry(models.Model):
    STATUS_CHOICES = (
        ('NEW', 'New'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    )
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Features**:
- **Status Tracking**: NEW → IN_PROGRESS → RESOLVED
- **Assignment**: Auto-assigned to receptionist (Melissa)
- **Timestamps**: `created_at` and `updated_at` for tracking

---

### 4. StaffProfile Model
**Purpose**: Extend User model for staff members like Melissa

```python
class StaffProfile(models.Model):
    ROLE_CHOICES = (
        ('RECEPTIONIST', 'Receptionist'),
        ('TOUR_GUIDE', 'Tour Guide'),
        ('MANAGER', 'Manager'),
        ('ADMIN', 'Admin'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True)
    can_receive_inquiries = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
```

**Role Types**:
- **RECEPTIONIST**: Handles inquiries (like Melissa)
- **TOUR_GUIDE**: Leads tours (like Shawn & Harry)
- **MANAGER**: Business oversight
- **ADMIN**: Full system access

---

## ✨ Features

### Public Features (Customer-Facing)

#### 1. Home Page
- **Hero Section**: Eye-catching gradient with CTA buttons
- **Services Grid**: Tours, rentals, group events
- **Pinterest Gallery**: 6 working Pinterest links with hover effects
- **CTA Section**: Book now call-to-action
- **Responsive**: Mobile-friendly navigation with hamburger menu

#### 2. Booking System
- **Form Fields**:
  - Customer name, email, phone
  - Activity selection (dropdown)
  - Date & time picker
  - Number of guests
  - Special notes
- **Validation**: Client-side and server-side
- **Conflict Detection**: Prevents double-booking
- **Confirmation**: Email notification (configurable)

#### 3. Contact/Inquiry System
- **Direct to Melissa**: Inquiries auto-assigned to receptionist
- **Fields**: Name, email, phone, subject, message
- **Status Tracking**: Admin can track inquiry progress
- **Response Management**: Staff can respond and mark resolved

#### 4. Activities Gallery
- **Dynamic Listing**: Shows all available activities
- **Pinterest Integration**: Working external gallery links
- **Filtering**: By type (TOUR/RENTAL)
- **Booking CTA**: Direct link to booking form

---

### Admin Features

#### 1. Django Admin Panel (`/admin/`)
- **Activity Management**: Add/edit/delete activities
- **Booking Management**: 
  - View all bookings
  - Filter by date, activity, confirmation status
  - Quick confirm/reject
  - Daily report generation
- **Inquiry Management**:
  - View all customer inquiries
  - Assign to staff
  - Update status (NEW/IN_PROGRESS/RESOLVED)
- **Staff Management**:
  - Add users like Melissa
  - Assign roles
  - Control inquiry routing

#### 2. Creating Staff Users (Melissa Example)
```python
# In Django shell or admin
from django.contrib.auth.models import User
from operations.models import StaffProfile

# Create user
melissa = User.objects.create_user(
    username='melissa',
    email='melissa@backyardadventures.com',
    first_name='Melissa',
    last_name='Smith',
    password='secure_password'
)

# Create staff profile
StaffProfile.objects.create(
    user=melissa,
    role='RECEPTIONIST',
    phone='(555) 123-4567',
    can_receive_inquiries=True,
    is_active=True
)
```

---

## 🎨 UI/UX Design

### Design Principles
1. **Minimalist**: Clean, uncluttered interface
2. **Mobile-First**: Responsive from 320px to 4K
3. **Accessible**: WCAG 2.1 AA compliant
4. **Performance**: < 2s page load time

### Color Palette
```css
:root {
    --primary-green: #7EC850;      /* Main brand color */
    --light-green: #A8E67D;        /* Accents */
    --dark-green: #5BA032;         /* Hover states */
    --accent-green: #E8F5E0;       /* Backgrounds */
    --text-dark: #2C3E2E;          /* Primary text */
    --text-light: #6B8068;         /* Secondary text */
    --white: #FFFFFF;
    --light-bg: #F8FDF5;           /* Page background */
}
```

### Typography
- **Font Family**: Nunito (Google Fonts)
- **Font Weights**: 300, 400, 600, 700, 800
- **Base Size**: 14px (0.875rem)
- **Headings**: 
  - H1: 2.5rem (40px)
  - H2: 2.2rem (35px)
  - H3: 1.5rem (24px)
  - H4: 1.1rem (18px)

### Responsive Breakpoints
```css
/* Mobile: 320px - 767px (default) */
/* Tablet: 768px - 1024px */
@media (max-width: 768px) { /* Tablet styles */ }

/* Desktop: 1025px+ */
@media (min-width: 1025px) { /* Desktop enhancements */ }
```

### Component Library

#### Buttons
```css
.btn {
    padding: 0.7rem 1.5rem;
    font-size: 0.9rem;
    font-weight: 600;
    border-radius: 30px;
    transition: all 0.3s ease;
    border: 2px solid var(--primary-green);
}

.btn-primary {
    background: var(--primary-green);
    color: var(--white);
}

.btn-outline {
    background: transparent;
    color: var(--primary-green);
}
```

#### Form Controls
```css
.form-control {
    padding: 0.7rem 1rem;
    font-size: 0.9rem;
    border: 2px solid #E8F5E0;
    border-radius: 8px;
    transition: border-color 0.3s;
}

.form-control:focus {
    outline: none;
    border-color: var(--primary-green);
}
```

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.12+
- pip (Python package manager)
- Git

### Local Development Setup
```bash
# 1. Clone repository
git clone <repository-url>
cd webapp

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create superuser (admin)
python manage.py createsuperuser

# 6. Run development server
python manage.py runserver

# 7. Access application
# Home: http://localhost:8000/
# Admin: http://localhost:8000/admin/
```

### Creating Test Data
```bash
python manage.py shell

# In shell:
from operations.models import Activity, StaffProfile
from django.contrib.auth.models import User

# Create activities
Activity.objects.create(
    name="River Kayaking Tour",
    type="TOUR",
    price=50.00,
    description="2-hour guided kayaking tour through scenic waterways",
    image_url="https://i.pinimg.com/564x/28/99/3a/28993a4639918f760170020616428d0b.jpg"
)

Activity.objects.create(
    name="Kayak Rental - Full Day",
    type="RENTAL",
    price=35.00,
    description="Full day kayak rental with all equipment included",
    image_url="https://i.pinimg.com/564x/67/86/36/678636/678636.jpg"
)

# Create Melissa
melissa = User.objects.create_user(
    username='melissa',
    email='melissa@backyardadventures.com',
    first_name='Melissa',
    last_name='Smith',
    password='melissa123'
)

StaffProfile.objects.create(
    user=melissa,
    role='RECEPTIONIST',
    phone='(555) 123-4567',
    can_receive_inquiries=True
)
```

---

## 🔧 Admin Panel

### Accessing Admin Panel
1. Navigate to `/admin/`
2. Login with superuser credentials
3. Manage all system data

### Admin Customizations

#### Activity Admin
```python
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price')
    list_filter = ('type',)
    search_fields = ('name', 'description')
```

#### Booking Admin (Melissa's Dashboard)
```python
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_email', 'activity', 'date', 'time', 'guests', 'is_confirmed', 'created_at')
    list_filter = ('is_confirmed', 'date', 'activity', 'created_at')
    search_fields = ('customer_name', 'customer_email', 'customer_phone')
    date_hierarchy = 'date'
    ordering = ('-date', '-time')
    list_editable = ('is_confirmed',)  # Quick confirmation
```

**Features**:
- **Morning Report**: Filter by today's date
- **Conflict View**: See all bookings for specific date
- **Quick Confirm**: Edit inline without opening form

#### Inquiry Admin
```python
@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status', 'assigned_to', 'created_at')
    list_filter = ('status', 'created_at', 'assigned_to')
    search_fields = ('name', 'email', 'subject', 'message')
    date_hierarchy = 'created_at'
    list_editable = ('status',)
    
    def save_model(self, request, obj, form, change):
        # Auto-assign to Melissa
        if not obj.assigned_to:
            receptionist = StaffProfile.objects.filter(
                role='RECEPTIONIST',
                can_receive_inquiries=True,
                is_active=True
            ).first()
            if receptionist:
                obj.assigned_to = receptionist.user
        super().save_model(request, obj, form, change)
```

---

## 🌐 API Endpoints

### Public URLs
```python
urlpatterns = [
    path('', home, name='home'),                                    # Landing page
    path('operations/book/', book_activity, name='book_activity'),  # Booking form
    path('operations/contact/', contact_us, name='contact_us'),     # Contact form
    path('operations/activities/', activities_gallery, name='activities_gallery'),  # Gallery
    path('admin/', admin.site.urls),                                # Admin panel
    path('dashboard/', include('analytics.urls')),                  # Analytics dashboard
]
```

### View Functions

#### Booking View
```python
def book_activity(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Booking Successful!')
                return redirect('home')
            except Exception as e:
                messages.error(request, f"Booking Failed: {e}")
    else:
        form = BookingForm()
    return render(request, 'operations/book.html', {'form': form})
```

#### Contact View (Auto-assign to Melissa)
```python
def contact_us(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            
            # Auto-assign to receptionist
            receptionist = StaffProfile.objects.filter(
                role='RECEPTIONIST',
                can_receive_inquiries=True,
                is_active=True
            ).first()
            
            if receptionist:
                inquiry.assigned_to = receptionist.user
            
            inquiry.save()
            messages.success(request, 'Thank you! Your inquiry has been sent.')
            return redirect('home')
    else:
        form = InquiryForm()
    return render(request, 'operations/contact.html', {'form': form})
```

---

## 🧪 Testing

### Manual Testing Checklist

#### Booking System
- [ ] Create booking without conflicts
- [ ] Attempt double-booking (should fail)
- [ ] Edit existing booking
- [ ] Confirm booking via admin
- [ ] View daily report in admin

#### Inquiry System
- [ ] Submit contact form
- [ ] Verify auto-assignment to Melissa
- [ ] Update inquiry status in admin
- [ ] Filter inquiries by status

#### UI/UX
- [ ] Test responsive design (mobile, tablet, desktop)
- [ ] Verify all Pinterest links work
- [ ] Check navigation menu (mobile hamburger)
- [ ] Validate form error messages
- [ ] Test success messages

### Automated Testing (Future Implementation)
```python
# tests.py example
from django.test import TestCase
from .models import Activity, Booking
from datetime import date

class BookingConflictTest(TestCase):
    def setUp(self):
        self.activity = Activity.objects.create(
            name="Test Tour",
            type="TOUR",
            price=50.00,
            description="Test"
        )
    
    def test_booking_conflict_prevention(self):
        # Create first booking
        Booking.objects.create(
            customer_name="John Doe",
            customer_email="john@example.com",
            activity=self.activity,
            date=date.today(),
            is_confirmed=True
        )
        
        # Attempt conflicting booking
        with self.assertRaises(ValidationError):
            conflicting_booking = Booking(
                customer_name="Jane Doe",
                customer_email="jane@example.com",
                activity=self.activity,
                date=date.today(),
                is_confirmed=True
            )
            conflicting_booking.save()
```

---

## 📦 Deployment

### Production Checklist
```python
# settings.py changes
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Deployment Steps
```bash
# 1. Collect static files
python manage.py collectstatic --noinput

# 2. Run database migrations
python manage.py migrate

# 3. Create superuser (production)
python manage.py createsuperuser

# 4. Start Gunicorn server
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

### Environment Variables
```bash
# .env file
SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_URL=postgresql://user:password@localhost/dbname
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

---

## 📝 Code Conventions

### Python Style Guide
- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions/classes
- Maximum line length: 100 characters

### Django Best Practices
- Use Django ORM (avoid raw SQL)
- Validate data in both forms and models
- Use Django messages framework for user feedback
- Keep views thin, models fat
- Use Django's built-in authentication

### Template Best Practices
- Extend base template
- Use template inheritance
- Keep logic in views, not templates
- Use `{% url %}` tags for URLs
- Escape user input (automatic in Django)

---

## 🤝 Contributing

### Adding New Features
1. Create feature branch: `git checkout -b feature/new-feature`
2. Make changes
3. Test thoroughly
4. Commit with descriptive message
5. Push and create pull request

### Database Migrations
```bash
# After model changes
python manage.py makemigrations
python manage.py migrate
```

---

## 📄 License

This project is proprietary software for Backyard Adventures, Jacksonville, Florida.

---

## 📞 Support

For technical support or questions:
- **Developer**: Contact development team
- **Business**: Shawn & Harry Weaver
- **Operations**: Melissa Smith

---

**Last Updated**: 2024-12-11
**Django Version**: 6.0
**Python Version**: 3.12+
