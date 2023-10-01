from flask import Blueprint, jsonify

homepage = Blueprint('homepage', __name__, url_prefix="/")

# Homepage
# /
@homepage.route("/", methods=["GET"])
def get_homepage():
    '''
    This route is the homepage route for the application that gives the user all of the available endpoints. Routes gated by
    admin authorisation are denoted by (admin) next to the route description.

    No database queries are performed in this route, all information is static.

    JWT is NOT required for the homepage.
    '''
    return jsonify({
        "01_Message": "Welcome to the fabrication catalogue app! Here you can find information about engineering design projects and where they can be fabricated internally. Below is a list of the application endpoints.",
        "02_Register_User": "POST /auth/register",
        "03_Login_User": "POST /auth/login",
        "04_Promote_To_Admin (admin)": "PATCH /auth/promote_to_admin/",
        "05_Update_User_Details": "PATCH /users/update_info",
        "06_Get_All_Users": "GET /users",
        "07_Get_User_by_ID": "GET /users/<id>",
        "08_Delete_User_by_ID (admin)": "DELETE /users/delete_user/<id>",
        "09_Get_Users_Comments": "GET /users/<id>/comments",
        "10_Create_Location (admin)": "POST /locations/",
        "11_Update_Location_by_ID (admin)": "PATCH /locations/<id>",
        "12_Get_All_Locations": "GET /locations",
        "13_Get_Location_by_ID": "GET /locations/<id>",
        "14_Delete_Location_by_ID (admin)": "DELETE /locations/delete_location/<id>",
        "15_Get_Location_Catalogue": "GET /locations/<id>/catalogue",
        "16_Post_Comment": "POST /comments",
        "17_Edit_Comment_by_ID": "PATCH /comments/<id>",
        "18_Get_All_Comments": "GET /comments",
        "19_Get_Comment_by_ID": "GET /comments/<id>",
        "20_Delete_Comment_by_ID": "DELETE /comments/delete_comment/<id>",
        "21_Create_Project (admin)": "POST /projects",
        "22_Update_Project_by_ID (admin)": "PATCH /projects/<id>",
        "23_Get_All_Projects": "GET /projects",
        "24_Get_Project_by_ID": "GET /projects/<id>",
        "25_Delete_Project_by_ID (admin)": "DELETE /projects/<id>",
        "26_Get_Manufactures_by_Project_ID": "GET /projects/<id>/suppliers",
        "27_Get_Drawings_by_Project_ID": "GET /projects/<id>/drawings",
        "28_Get_Comments_by_Project_ID": "GET /projects/<id>/comments",
        "29_Create_Manufacture (admin)": "POST /manufactures",
        "30_Update_Manufacture_by_ID (admin)": "PATCH /manufactures/loc/<id1>/proj/<id2>",
        "31_Get_All_Manufactures": "GET /manufactures",
        "32_Get_Manufacture_by_ID": "GET /manufactures/loc/<id1>/proj/<id2>",
        "33_Delete_Manufacture_by_ID (admin)": "DELETE /manufactures/loc/<id1>/proj/<id2>",
        "34_Create_Drawing (admin)": "POST /drawings",
        "35_Update_Drawing_by_ID (admin)": "PATCH /drawings/<id>",
        "36_Get_All_Drawings": "GET /drawings",
        "37_Get_Drawing_by_ID": "GET /drawings/<id>",
        "38_Delete_Drawing_by_ID (admin)": "DELETE /drawings/delete_drawing/<id>",
        "39_Create_Country (admin)": "POST /countries",
        "40_Update_Country_by_ID (admin)": "PUT /countries/<id>",
        "41_Get_All_Countries": "GET /countries",
        "42_Get_Country_by_ID": "GET /countries/<id>",
        "43_Delete_Country_by_ID (admin)": "DELETE /countries/delete_country/<id>",
        "44_Create_Location_Type (admin)": "POST /location-types",
        "45_Update_Location_Type_by_ID (admin)": "PUT /location-types/<id>",
        "46_Get_All_Location_Types": "GET /location-types",
        "47_Get_Location_Type_by_ID": "GET /location-types/<id>",
        "48_Delete_Location_Type_by_ID (admin)": "DELETE /location-types/delete_loc_type/<id>",
        "49_Create_Currency (admin)": "POST /currencies",
        "50_Update_Currency_by_ID (admin)": "PUT /currencies/<id>",
        "51_Get_All_Currencies": "GET /currencies",
        "52_Get_Currency_by_ID": "GET /currencies/<id>",
        "53_Delete_Currency_by_ID (admin)": "DELETE /currencies/delete_currency/<id>"
    })