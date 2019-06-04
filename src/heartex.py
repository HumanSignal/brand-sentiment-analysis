"""
"""
import requests

URL = "https://go.heartex.net"


def create_project(token=None, name="Project", label_config=None):
    """
    """
    # create a project
    res = requests.post(URL + '/api/projects/', data={
        "title": name,
        "label_config": label_config
    }, headers={
        "Authorization":"Token %s" % (token,) 
    })
    
    return res.json()['id']
    
def upload_data(token=None, project=None, input=None):
    """
    """
    files = {}
    files[input] = open(input, 'rb')
    res = requests.post(URL + '/api/projects/%d/tasks/bulk/' % (project,),
                        files=files,
                        # json={"data": "file"}
                        headers={
                            "Authorization":"Token %s" % (token,) 
                        })
    
    return res

def publish_project(token=None, project=None):
    """
    """
    res = requests.patch(URL + '/api/projects/%d/' % (project,),
                         data={ "is_published": True },
                         headers={
                             "Authorization":"Token %s" % (token,) 
                         })
    
    return res

def run_predict(token=None, project=None, data=None, *args, **kwargs):
    """
    """
    assert project is not None, 'Specify project number in heartex'
    assert token is not None, 'Specify your token to heartex'
    assert data is not None, 'Data must be set'
    res = requests.post(URL + '/api/projects/%d/predict/' % (project,),
                        json=data,
                        headers={
                            "Content-Type": "application/json",
                            "Authorization":"Token %s" % (token,) 
                        })
    
    return res

def new_project_setup(token=None, label_config=None, input=None, name=None,
                      *args, **kwargs):
    """
    """
    pk = create_project(token=token, label_config=label_config, name=name)
    
    upload_data(token=token, input=input, project=pk)
    publish_project(token=token, project=pk)
    
    return pk

