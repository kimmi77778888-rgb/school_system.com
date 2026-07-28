"""
Utility functions for the school app
"""
from user_agents import parse


def get_client_ip(request):
    """Extract client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def parse_user_agent(request):
    """Parse user agent string to extract device information"""
    user_agent_string = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse(user_agent_string)
    
    # Determine device type
    if user_agent.is_mobile:
        device_type = 'Mobile'
    elif user_agent.is_tablet:
        device_type = 'Tablet'
    elif user_agent.is_pc:
        device_type = 'Desktop'
    else:
        device_type = 'Unknown'
    
    # Get device details
    device_family = user_agent.device.family
    device_brand = user_agent.device.brand
    device_model = user_agent.device.model
    
    # Build device name
    device_name_parts = []
    if device_brand and device_brand != 'Generic':
        device_name_parts.append(device_brand)
    if device_model and device_model != 'Generic':
        device_name_parts.append(device_model)
    elif device_family and device_family not in ['Other', 'Generic Smartphone', 'Generic']:
        device_name_parts.append(device_family)
    
    device_name = ' '.join(device_name_parts) if device_name_parts else device_type
    
    # Get browser info
    browser = f"{user_agent.browser.family} {user_agent.browser.version_string}"
    
    # Get OS info
    os = f"{user_agent.os.family} {user_agent.os.version_string}"
    
    return {
        'device_type': device_type,
        'device_name': device_name,
        'browser': browser,
        'operating_system': os,
        'user_agent': user_agent_string,
        'is_mobile': user_agent.is_mobile,
        'is_tablet': user_agent.is_tablet,
        'is_pc': user_agent.is_pc,
    }


def create_login_notification(user, login_history):
    """Create a notification for admins when someone logs in"""
    from .models import Notification, UserProfile
    
    # Get device icon
    device_icon = '📱' if login_history.device_type == 'Mobile' else '💻' if login_history.device_type == 'Desktop' else '📲'
    
    # Build notification message
    role = user.profile.role if hasattr(user, 'profile') else 'User'
    role_khmer = {
        'admin': 'អ្នកគ្រប់គ្រង',
        'teacher': 'គ្រូបង្រៀន',
        'parent': 'មាតាបិតា',
        'student': 'សិស្ស',
    }.get(role, 'អ្នកប្រើ')
    
    message = f"""
{device_icon} ការចូលប្រើប្រាស់ថ្មី

អ្នកប្រើ: {user.get_full_name() or user.username}
តួនាទី: {role_khmer}
ឧបករណ៍: {login_history.device_name}
ប្រភេទ: {login_history.device_type}
Browser: {login_history.browser}
OS: {login_history.operating_system}
IP: {login_history.ip_address}
ពេលវេលា: {login_history.login_time.strftime('%d/%m/%Y %H:%M:%S')}
    """.strip()
    
    # Create notification for all admins
    Notification.objects.create(
        title=f"ការចូលប្រើថ្មី - {user.username}",
        message=message,
        notification_type='info',
        audience='admin',
    )
