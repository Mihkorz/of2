# -*- coding: utf-8 -*-

import csv

from django import forms
from django.conf import settings



def validate_file(file_, content_types=None, max_upload_size=None):
    """return True of raise ValidationError
    
    Validates uploaded file to check Columns and Empty rows
    
    """  
    
    try:
        file_type = file_._content_type

        if file_type not in settings.PATIENT_UPLOAD_FILES_CONTENT_TYPES:
            raise forms.ValidationError(u'File format "%s" is not supported!'
                                        % file_type)
        
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(file_.read(), delimiters='\t,;')
        file_.seek(0)
        allrows = csv.reader(file_, dialect='excel', delimiter=dialect.delimiter)

        for row in allrows:
            if not any(row): # if not all(row)
                raise forms.ValidationError(u'File contains an empty row! \
                                              Presumably row number %s \
                                              Please check your file and try \
                                              uploading it again.'
                                        % allrows.line_num)
                
        
                
    except:
        raise 

    
    return True