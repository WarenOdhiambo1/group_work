from django.shortcuts import render

# Create your views here.
import matplotlib.pyplot as plt
import pandas as pd
import io
import urllib, base64
from django.shortcuts import render
from operations.models import Booking

def dashboard(request):
    # 1. GET DATA FROM SQL (Using Django ORM)
    # We pull all bookings from the DB
    bookings = Booking.objects.all().values()
    
    if not bookings:
        return render(request, 'dashboard_empty.html')

    # 2. LOAD INTO PANDAS
    df = pd.DataFrame(bookings)
    
    # 3. ANALYSIS: Count bookings per Activity
    # "Rental Patterns"
    activity_counts = df['activity_id'].value_counts()

    # 4. VISUALIZE WITH MATPLOTLIB
    plt.figure(figsize=(10,6))
    activity_counts.plot(kind='bar', color='orange')
    plt.title('Popularity of Tours vs Rentals')
    plt.xlabel('Activity ID')
    plt.ylabel('Number of Bookings')
    
    # 5. CONVERT IMAGE TO HTML STRING (No saving to file)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    
    return render(request, 'dashboard.html', {'data': uri})