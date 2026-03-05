from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib import messages
import time

class SessionTimeoutMiddleware:
    """
    Middleware to handle 30-minute session timeout
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is authenticated
        if request.user.is_authenticated:
            # Get last activity time from session
            last_activity = request.session.get('last_activity')
            current_time = time.time()
            
            # If this is the first request, set last activity
            if last_activity is None:
                request.session['last_activity'] = current_time
            else:
                # Check if session has expired (30 minutes = 1800 seconds)
                if current_time - last_activity > 1800:
                    # Session expired, logout user
                    logout(request)
                    messages.warning(request, 'Your session has expired. Please log in again.')
                    # Redirect to login page
                    return redirect('login')
                else:
                    # Update last activity time
                    request.session['last_activity'] = current_time

        response = self.get_response(request)
        return response
