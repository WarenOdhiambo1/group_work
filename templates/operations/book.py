{% extends 'base.html' %}

{% block content %}
<div class="container" style="max-width: 600px; padding: 50px 20px;">
    
    <div class="card" style="padding: 40px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1);">
        <h2 style="text-align: center; color: #FFB347; margin-bottom: 20px;">Book Your Adventure</h2>
        <p style="text-align: center; color: #666; margin-bottom: 30px;">
            Secure your spot for a tour or equipment rental.
        </p>

        {% if messages %}
            {% for message in messages %}
                <div style="padding: 15px; margin-bottom: 20px; border-radius: 5px; 
                            background: {% if message.tags == 'success' %}#d4edda{% else %}#f8d7da{% endif %}; 
                            color: {% if message.tags == 'success' %}#155724{% else %}#721c24{% endif %};">
                    {{ message }}
                </div>
            {% endfor %}
        {% endif %}

        <form method="post">
            {% csrf_token %}
            
            <div style="margin-bottom: 20px;">
                <label style="font-weight: bold; display: block; margin-bottom: 5px;">Full Name</label>
                {{ form.customer_name }}
            </div>

            <div style="margin-bottom: 20px;">
                <label style="font-weight: bold; display: block; margin-bottom: 5px;">Email Address</label>
                {{ form.customer_email }}
            </div>

            <div style="margin-bottom: 20px;">
                <label style="font-weight: bold; display: block; margin-bottom: 5px;">Select Activity</label>
                {{ form.activity }}
            </div>

            <div style="margin-bottom: 20px;">
                <label style="font-weight: bold; display: block; margin-bottom: 5px;">Date</label>
                {{ form.date }}
            </div>

            {% if form.errors %}
                <div style="color: red; margin-bottom: 20px;">
                    {{ form.non_field_errors }}
                </div>
            {% endif %}

            <button type="submit" class="btn btn-solid" style="width: 100%; background: #FFB347; border: none;">
                Confirm Registration
            </button>
        </form>
    </div>
</div>

<style>
    /* Styling for the Django Form inputs */
    .form-control {
        width: 100%;
        padding: 12px;
        border: 1px solid #ddd;
        border-radius: 8px;
        box-sizing: border-box; /* Fix padding issue */
    }
</style>
{% endblock %}