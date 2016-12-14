# -*- coding: utf-8 -*-

import csv
from tempfile import NamedTemporaryFile

from django import forms
from django.conf import settings

from pandas import read_csv


def validate_input_document(doc_file):
    """
    Raises ValidationError if something is wrong.
    """
    if hasattr(doc_file, 'content_type'):
        content_type = doc_file.content_type
        if content_type not in settings.PATIENT_UPLOAD_FILES_CONTENT_TYPES:
            raise forms.ValidationError(u'File format "%s" is not supported!'% content_type)

    doc_file.seek(0)

    with NamedTemporaryFile(mode='w+', delete=True) as temp_doc:
        temp_doc.write(doc_file.read())
        temp_doc.flush()
        temp_doc.seek(0)

        _validate_file(temp_doc)


def _validate_file(file_,):
    """
    Raises ValidationError if something is wrong.
    """
    sniffer = csv.Sniffer()
    dialect = sniffer.sniff(file_.read(), delimiters='\t,;')

    file_.seek(0)

    df = read_csv(file_, delimiter=dialect.delimiter)

    # TODO: col.strip() == 'SYMBOL' or 'Name'?
    symbol = [col for col in df.columns if 'SYMBOL' in col]
    name = [col for col in df.columns if 'Name' in col]
    if not symbol and not name:
        raise forms.ValidationError(u"Document doesn't contain 'SYMBOL' or 'Name' column.")

    for col_name in df.columns:
        try:
            df[col_name].astype(float)
        except ValueError as e:
            raise forms.ValidationError(
                u'Document contains non-float value in column "%s". Error: %s' % (col_name, e)
            )

    # In fact zeros may present in DataFrame.
    """ Check for zeros in DataFrame
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
