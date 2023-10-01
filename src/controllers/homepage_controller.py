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
        "02_Register_User": "/auth/register",
        "03_Login_User": "/auth/login",
        "04_Promote_To_Admin (admin)": "/auth/promote_to_admin/",
        "05_Update_User_Details": "/users/update_info",
        "06_Get_All_Users": "/users",
        "07_Get_User_by_ID": "/users/<id>",
        "08_Delete_User_by_ID (admin)": "/users/delete_user/<id>",
        "09_Get_Users_Comments": "/users/<id>/comments",
        "10_Create_Location (admin)": "/locations/",
        "11_Update_Location_by_ID (admin)": "/locations/<id>",
        "12_Get_All_Locations": "/locations",
        "13_Get_Location_by_ID": "/locations/<id>",
        "14_Delete_Location_by_ID (admin)": "/locations/delete_location/<id>",
        "15_Get_Location_Catalogue": "/locations/<id>/catalogue",
        "16_Post_Comment": "/comments",
        "17_Edit_Comment_by_ID": "/comments/<id>",
        "18_Get_All_Comments": "/comments",
        "19_Get_Comment_by_ID": "/comments/<id>",
        "20_Delete_Comment_by_ID": "/comments/delete_comment/<id>",
        "21_Create_Project (admin)": "/projects",
        "22_Update_Project_by_ID (admin)": "/projects/<id>",
        "23_Get_All_Projects": "/projects",
        "24_Get_Project_by_ID": "/projects/<id>",
        "25_Delete_Project_by_ID (admin)": "/projects/<id>",
        "26_Get_Manufactures_by_Project_ID": "/projects/<id>/suppliers",
        "27_Get_Drawings_by_Project_ID": "/projects/<id>/drawings",
        "28_Get_Comments_by_Project_ID": "/projects/<id>/comments",
        "29_Create_Manufacture (admin)": "/manufactures",
        "30_Update_Manufacture_by_ID (admin)": "/manufactures/loc/<id1>/proj/<id2>",
        "31_Get_All_Manufactures": "/manufactures",
        "32_Get_Manufacture_by_ID": "/manufactures/loc/<id1>/proj/<id2>",
        "33_Delete_Manufacture_by_ID (admin)": "/manufactures/loc/<id1>/proj/<id2>",
        "34_Create_Drawing (admin)": "/drawings",
        "35_Update_Drawing_by_ID (admin)": "/drawings/<id>",
        "36_Get_All_Drawings": "/drawings",
        "37_Get_Drawing_by_ID": "/drawings/<id>",
        "38_Delete_Drawing_by_ID (admin)": "/drawings/delete_drawing/<id>",
        "39_Create_Country (admin)": "/countries",
        "40_Update_Country_by_ID (admin)": "/countries/<id>",
        "41_Get_All_Countries": "/countries",
        "42_Get_Country_by_ID": "/countries/<id>",
        "43_Delete_Country_by_ID (admin)": "/countries/delete_country/<id>",
        "44_Create_Location_Type (admin)": "/location-types",
        "45_Update_Location_Type_by_ID (admin)": "/location-types/<id>",
        "46_Get_All_Location_Types": "/location-types",
        "47_Get_Location_Type_by_ID": "/location-types/<id>",
        "48_Delete_Location_Type_by_ID (admin)": "/location-types/delete_loc_type/<id>",
        "49_Create_Currency (admin)": "/currencies",
        "50_Update_Currency_by_ID (admin)": "/currencies/<id>",
        "51_Get_All_Currencies": "/currencies",
        "52_Get_Currency_by_ID": "/currencies/<id>",
        "53_Delete_Currency_by_ID (admin)": "/currencies/delete_currency/<id>"
    })