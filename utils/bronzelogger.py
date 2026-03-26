import requests
from Rahul.settings import DEBUG

def addrecord(action_function_name, request):
    # dont log in debug mode
    if DEBUG:
        return 200, "debug mode active"
    
    school_mate_map = {
        'all_current_terms':'Checking terms',
        'marksheet_view':'Viewing marksheet',
        'student_scorecard':'Viewing student scorecard',
        'scorecard_pdf_download':'Downloading scorecard',
        'checks_index':'Notebook checking class list',
        'list_checks':'Listing all checks of a class',
        'nb_checking':'Notebook checking interface',
        'student_checks_detail':'Viewing student notebook check details',
        'all_students':'Listing all students for notebook checking',
        'class_list':'Listing all classes',
        'student_detail':'Viewing student details',
        'student_create':'Creating a new student',
        'student_edit':'Editing student details',
        'student_delete':'Deleting a student',
        'student_list_by_batch':'Listing students by batch',
    }

    portfolio_map = {
        'index':'Homepage',
        'projects':'Projects page',
        'v2':'Version 2 of portfolio',
        'v1':'Version 1 of portfolio',
        'schoolmate_landing':'Schoolmate landing page',
        'codebunny_landing':'Codebunny landing page',
    }

    source = ""
    action_map = {}
    if action_function_name in school_mate_map:
        source = "Schoolmate"
        action_map = school_mate_map
    elif action_function_name in portfolio_map:
        source = "Portfolio"
        action_map = portfolio_map
    else:
        source = "Others"
    try:
        url = "https://rahul-jangra-leonado10000.vercel.app/cmd/addrecord"
        res = requests.post(
            url,
            data={
                'userip': request.META.get('REMOTE_ADDR', ''),
                'actionmessage': action_map.get(action_function_name, ''),
                'source': source,
                'user': request.user.username if request.user.is_authenticated else 'Anonymous',
            }
        )
        return 200, "success"
    except Exception as e:
        return 500, str(e)
    
def bronzelogger(func):
    def wrapper(*args, **kwargs):
        a,b = addrecord(func.__name__, args[0])
        return func(*args, **kwargs)
    return wrapper