def getform(theform, valuelist, notpresent='', nolist=False):
    """
    This function, given a CGI form as a
    FieldStorage instance, extracts the
    data from it, based on valuelist
    passed in. Any non-present values are
    set to '' - although this can be
    changed. (e.g. to return None so you
    can test for missing keywords - where
    '' is a valid answer but to have the
    field missing isn't.) It also takes a
    keyword argument 'nolist'. If this is
    True list values only return their
    first value.
    """
    data = {}
    for field in valuelist:
        if not theform.has_key(field):
        #  if the field is not present (or was empty)
            data[field] = notpresent
        else: 
        # the field is present
            if  type(theform[field]) != type([]):           
            # is it a list or a single item
                data[field] = theform[field].value
            else:
                if not nolist:                               
                # do we want a list ?
                    data[field] = theform.getlist(field)     
                else:
                    data[field] = theform.getfirst(field)     
                    # just fetch the first item 
            return data

def getall(theform, nolist=False):
    """
    Passed a form (cgi.FieldStorage
    instance) return *all* the values.
    This doesn't take into account
    multipart form data (file uploads).
    It also takes a keyword argument
    'nolist'. If this is True list values
    only return their first value.
    """
    data = {}
    for field in theform.keys():                
    # we can't just iterate over it, but must use the keys() method
        if type(theform[field]) ==  type([]):
            if not nolist:
                data[field] = theform.getlist(field)
            else:
                data[field] = theform.getfirst(field)
        else:
            data[field] = theform[field].value
    return data

def isblank(indict):
    """
    Passed an indict of values it checks
    if any of the values are set. Returns
    True if the indict is empty, else
    returns False. I use it on the a form
    processed with getform to tell if my
    CGI has been activated without any
    form values.
    """
    for key in indict.keys():
        if indict[key]:
            return False
    return True 
