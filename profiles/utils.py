# -*- coding: utf-8 -*-

import csv
import numpy as np

from django import forms
from django.conf import settings

from pandas import read_csv, read_excel, DataFrame



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
        
        df = read_csv(file_, delimiter=dialect.delimiter)
        symbol = [col for col in df.columns if 'SYMBOL' in col]
        name = [col for col in df.columns if 'Name' in col]
        tumour_cols = [col for col in df.columns if 'Tumour' in col]
        norm_cols = [col for col in df.columns if 'Norm' in col]
        
        if not symbol and not name:
            raise forms.ValidationError(u"Document doesn't contain 'SYMBOL' or 'Name' column.\
                                         Please check your document and try uploading it again.")
            
        for tumour in tumour_cols:
            try:
                df[tumour].astype(float)
            except ValueError as e:
                raise forms.ValidationError(u'Document contains Sample with non float value in column %s. Error: %s'
                                        %  (tumour, e))
                
        for norm in norm_cols:
            try:
                df[norm].astype(float)
            except :
                raise forms.ValidationError(u'Document contains Norm with non float value in column %s.'
                                        % norm)
        """Check for zeros in DataFrame
        check_zeros = df.apply(lambda x: np.any(x==0))
        zeros = check_zeros[check_zeros]
        if len(zeros.index)>0:
            raise forms.ValidationError(u'Document contains Zero values in column(s): %s.'
                                         %(', '.join(list(zeros.index.values))))
            
                
        
        """
        """
        allrows = csv.reader(file_, dialect='excel', delimiter=dialect.delimiter)

        for row in allrows:
            if not any(row): # if not all(row)
                raise forms.ValidationError(u'File contains an empty row! \
                                              Presumably row number %s. \
                                              Please check your file and try \
                                              uploading it again.'
                                        % allrows.line_num)
        """
                
        
                
    except:
        raise 

    
    return True