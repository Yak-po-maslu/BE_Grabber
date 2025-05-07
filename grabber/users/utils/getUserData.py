from users.models import CustomUser

def get_user_data(user:CustomUser):
    user_data = dict()
    user_data['id'] = user.id
    user_data['phone_number'] = user.phone_number
    user_data['email'] = user.email
    user_data['first_name'] = user.first_name
    user_data['last_name'] = user.last_name
    user_data['role'] = user.role
    user_data['location'] = user.location
    user_data['date_joined'] = user.date_joined
    user_data['last_login'] = user.last_login
    return user_data
