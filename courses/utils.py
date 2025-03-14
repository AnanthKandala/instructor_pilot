import os
from dotenv import load_dotenv

import autocanvas.core as ac
from autocanvas.config import INPUT_DIR, OUTPUT_DIR, get_API_key
from canvasapi import Canvas

def get_canvas_url():
    """
    Return the Canvas URL, appending a trailing slash if needed.
    """
    load_dotenv()
    if os.getenv("API_URL") is not None:
        api_url =  os.getenv("API_URL")
    else:
        api_url = "https://ufl.instructure.com/"
    
    if api_url[-1] != "/":
        api_url += "/"
    return api_url

API_URL = get_canvas_url()
CANVAS_API_KEY = get_API_key()

def get_canvas_object():
    """
    Return a Canvas object.
    """
    return Canvas(API_URL, CANVAS_API_KEY)

def get_canvas_course(course_code=None, term_name=None, canvas_id=None):
    """
    Return a Canvas course object from a database course.
    """ 
    list_to_include = [
            "course_image","observed_users",
            "teachers","total_students",
            "sections","course_progress",
            "term","public_description"]
    canvas = get_canvas_object()
    if canvas_id is not None:
        return canvas.get_course(
            int(canvas_id), 
            use_sis_id=False,
            include=list_to_include)
    canvas_courses = canvas.get_courses( 
        include=list_to_include)

    # TODO: much more info is available in the Canvas API
    # so we can add some more columns to the database
    for canvas_course in canvas_courses:
        try:
            if (canvas_course.course_code == course_code 
                    and canvas_course.term["name"] == term_name):
                return canvas_course
        except:
            pass
    return None
    

def canvas_users_df(canvas_course):
    """
    Return a Pandas DataFrame of users in a course.
    """
    df_TAs, df_teachers = ac.course_info.get_teaching_personel(
        canvas_course, 
        add_first_name=True, 
        groups=["teacher", "ta"])

    df_students, df_sections = ac.course_info.get_students_from_sections(
                                    canvas_course, add_TA_info=False)
    return df_TAs, df_teachers, df_students, df_sections