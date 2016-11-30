import logging

from pandas import read_excel

from core.models import Pathway, Gene, Node, Component, Relation


def maxim_format_pathway(filepath, organism, database, message_log):
    """
    Add new pathway to OF database
    using Maxim pathway file format
    Format: Excel file with corresponding sheetnames

    All code with 'apply' functions is wrapped in try-except for debugging reasons if needed
    """

    log = logging.getLogger('oncoFinder')

    file_name = filepath.split('/')[-1]  # split filepath and get last element as filename
    pathname = file_name.replace('.xls', '').replace(' ', '_')  # get pathname from filename

    try:  # check if pathway already exists
        new_path = Pathway.objects.get(name=pathname, organism=organism, database=database)
    except:  # if not, add new
        msg = 'Missing pathway ({}, {}, {})'.format(pathname, organism, database)
        log.info(msg, exc_info=1)
        if message_log:
            message_log.info(msg)

        new_path = Pathway(name=pathname, amcf=0, organism=organism, database=database)
        new_path.save()

    ##############################################################################
    # Add Genes
    ##############################################################################

    def add_gene(row, path):
        if row['arr'] != 'missing':
            g = Gene(name=row['gene'], arr=row['arr'], pathway=path)
            g.save()

    try:
        df_genes = read_excel(filepath, sheetname='genes', header=None).fillna('missing')
        df_genes.columns = ['gene', 'arr']
        df_genes.apply(add_gene, axis=1, path=new_path)
    except:
        msg = 'Failed to load genes from Excel file "{}".'.format(filepath)
        log.warning(msg, exc_info=1)
        if message_log:
            message_log.error(msg)

    ##############################################################################
    # Add Nodes and Components. Update Node names
    ##############################################################################

    def add_node_and_components(row, path):

        node_name = row.name
        try:
            new_node = Node.objects.get(name=node_name, pathway=path)
        except:
            log.info('Missing node ({}, {})'.format(node_name, path), exc_info=1)
            new_node = Node(name=node_name, pathway=path)
            new_node.save()
        row = row[row != 1]
        row.dropna(inplace=True)  # taking into account different row lengths for different nodes
        for component in row:
            new_component = Component(name=component, node=new_node)
            new_component.save()

    try:
        df_nodes = read_excel(filepath, sheetname='nodes', header=None, index_col=0)
        df_nodes.drop(1, axis=1, inplace=True)
        df_nodes_name = df_nodes[2]

        # Node name = name of the first component in row
        # see file for more details

        df_nodes.apply(add_node_and_components, axis=1, path=new_path)
    except:
        msg = 'Failed to load nodes from Excel file "{}".'.format(filepath)
        log.warning(msg, exc_info=1)
        if message_log:
            message_log.error(msg)

    # Update Node names

    def update_node_name(row, path):
        name = row.name
        normal_name = row['new name']

        node = Node.objects.get(name=name, pathway=path)
        node.name = normal_name
        node.save()

    try:
        df_node_names = read_excel(filepath, sheetname='node_names', header=None, index_col=0)
        df_node_names.columns = ['new name']
        df_node_names.apply(update_node_name, axis=1, path=new_path)
    except:
        msg = 'Failed to load node_names from Excel file "{}".'.format(filepath)
        log.warning(msg, exc_info=1)
        if message_log:
            message_log.error(msg)

    ##############################################################################
    # Add Relations
    ##############################################################################

    def add_relation(row, sNodes, path):
        from_node_name = row['from']
        to_node_name = row['to']

        reltype = 2  # default value=2(unknown) to draw black arrows
        if row['reltype'] == 'activation':
            reltype = 1
        if row['reltype'] == 'inhibition':
            reltype = 0
        if row['reltype'] == 'unknown':
            reltype = 2

        db_node_from = Node.objects.get(name=from_node_name, pathway=path)
        db_nodeto = Node.objects.get(name=to_node_name, pathway=path)

        nrel = Relation(fromnode=db_node_from, tonode=db_nodeto, reltype=reltype)
        nrel.save()

    try:
        df_rels = read_excel(filepath, sheetname='edges', header=None)
        df_rels.columns = ['from', 'to', 'reltype']
        df_rels.apply(add_relation, axis=1, sNodes=df_nodes_name, path=new_path)
    except:
        msg = 'Failed to load edges from Excel file "{}".'.format(filepath)
        log.warning(msg, exc_info=1)
        if message_log:
            message_log.error(msg)
