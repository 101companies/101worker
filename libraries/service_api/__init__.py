
def expand_data(data):
    if data['type'] == 'folders':
            folders = data['data']
            folders = map(lambda folder: os.path.join('/tmp/', folder), folders)
            data['data'] = []
            for folder in folders:
                for root, subFolders, files in os.walk(folder):
                    for file in files:
                        f = os.path.join(root,file)
                        data['data'].append(f)
    return data
