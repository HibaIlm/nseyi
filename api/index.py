from flask import Flask, request, jsonify,json
from supabase import create_client, Client


app = Flask(__name__)

url = "https://hljaiwqvdchahyfsvpdh.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhsamFpd3F2ZGNoYWh5ZnN2cGRoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDI0NjM1MzUsImV4cCI6MjAxODAzOTUzNX0.3CioZ51QSifNdWya5a_h4jhOxx_Qp4f79GhsuNNTCl0"

supabase: Client = create_client(url, key)

@app.route('/users.signup', methods=['POST', 'GET'])
def api_users_signup():
    try:

        Email = request.form.get('email')
        Name = request.form.get('name')
        Password = request.form.get('password')
        Location = request.form.get('location')
        Phone = request.form.get('phone')
        error =False

        
        if (not Email) or (len(Email) < 5):
            error = 'Email needs to be valid'

        if (not Name) or (len(Name) == 0):
            error = 'Name cannot be empty'

        if (not error) and ((not Password) or (len(Password) < 6)):
            error = 'Provide a password'

        if (not error):
            response = supabase.table('User').select("*").ilike('Email', Email).execute()
            if len(response.data) > 0:
                error = 'User already exists'

        if (not error):
            response = supabase.table('User').insert({
                "Email": Email,
                "Password": Password,
                "Name": Name,
                "Location": Location,
                "Phone": Phone
            }).execute()
            print(str(response.data))
            if len(response.data) == 0:
                error = 'Error creating the user'

        if error:
            return jsonify({'status': 500, 'message': error})

        return jsonify({'status': 200, 'message': '', 'data': response.data[0]})

    except Exception as e:
        return jsonify({'status': 500, 'message': f'Internal Server Error: {str(e)}'})


@app.route('/users.login', methods=['POST', 'GET'])
def api_users_login():
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        error = False

        if (not email) or (len(email) < 5):
            error = 'Email needs to be valid'

        if (not error) and ((not password) or (len(password) < 5)):
            error = 'Provide a password'

        if (not error):
            response = supabase.table('User').select("*").ilike('Email', email).eq('Password', password).execute()
            if len(response.data) > 0:
                return jsonify({'status': 200, 'message': '', 'data': response.data[0]})

        if not error:
            error = 'Invalid Email or password'

        return jsonify({'status': 500, 'message': error})

    except Exception as e:
        return jsonify({'status': 500, 'message': f'Internal Server Error: {str(e)}'})
    
        
@app.route('/users.changePassword', methods=['PUT'])
def api_users_change_password():
    phone = request.form.get('phone')
    new_password = request.form.get('newPassword')
    error = False

    # Validate phone
    if (not phone) :
        error = 'Phone needs to be valid'
     # Convert phone to integer
    phone_as_int = int(phone) if phone.isdigit() else None       

    # Validate new password
    if (not error) and ((not new_password) or (len(new_password) < 5)):
        error = 'Provide a valid new password'

    # Update the password in the Supabase database
    if not error:
        response = supabase.table('User').update({"Password": new_password}).eq('Phone', phone_as_int).execute()
        if len(response.data) == 0:
            error = 'Error updating the password'

    if error:
        return json.dumps({'status': 400, 'message': error})

    return json.dumps({'status': 200, 'message': 'Password updated successfully'})

@app.route('/cook.post', methods=['POST', 'GET'])
def api_post_dish():
    cookID = request.form.get('cookID')
    name = request.form.get('name')
    description = request.form.get('description')
    Start_date = request.form.get('Start_date')
    End_date = request.form.get('End_date')
    price = request.form.get('price')
    Dish_pic = request.form.get('Dish_pic')
    error = None

    if (not name) or (len(name) == 0):
        error = 'Name cannot be empty'

    if (not cookID) or (len(cookID) == 0):
        error = 'CookID cannot be empty'

    if error:
        return json.dumps({'status': 500, 'message': error})

    response = supabase.table('Dish').insert({
        "Dish_Name": name,
        'Cook_ID': cookID,
        'Dish_Pic': Dish_pic,
        'Dish_Desc': description,
        'TimeAvailabilityStart': Start_date,
        'TimeAvailabilityEnd': End_date,
        'Dish_Price': price,
    }).execute()

    print(str(response.data))

    if len(response.data) == 0:
        error = 'Error '

    if error:
        return json.dumps({'status': 500, 'message': error})

    return json.dumps({'status': 200, 'message': '', 'data': response.data[0] if response.data else []})

@app.route('/cook.register', methods=['POST', 'GET'])
def api_register_cook():
    UserID = request.form.get('UserID')
    CookName = request.form.get('CookName')
    Bio = request.form.get('Bio')
    Profile_pic = request.form.get('Profile_pic')
    error = None

    if (not CookName) or (len(CookName) == 0):
        error = 'Name cannot be empty'
        
    if (not UserID) or (len(UserID) == 0):
        error = 'User ID cannot be empty'

    if error:
        return json.dumps({'status': 500, 'message': error})

    response = supabase.table('Cook').insert({
        "Cook_Name": CookName,
        'User_ID': UserID,
        'Profile_Pic': Profile_pic,
        'Bio': Bio,

    }).execute()

    print(str(response.data))

    if len(response.data) == 0:
        error = 'Error '

    if error:
        return json.dumps({'status': 500, 'message': error})

    return json.dumps({'status': 200, 'message': '', 'data': response.data[0] if response.data else []})

               
@app.route('/')
def about():
    return 'Welcome to benet eddar'


if __name__ == "__main__":
    app.run(debug=True)
