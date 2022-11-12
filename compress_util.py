import os
import zipfile
import re

allowed_file_extensions = {'.py', 'LICENSE'}


def zipdir(path, ziph: zipfile.ZipFile, zip_subdir_name):
    for root, dirs, files in os.walk(path):
        for file in files:
            if any(file.endswith(ext) for ext in allowed_file_extensions):
                orig_hier = os.path.join(root, file)
                arc_hier = os.path.join(zip_subdir_name, orig_hier)
                ziph.write(orig_hier, arc_hier)


def generate_zip_filename(addon_name):
    major, minor, patch = get_addon_version('__init__.py')
    return '{}-{}-{}-{}.zip'.format(addon_name, major, minor, patch)


def get_addon_version(init_path):
    version_reg = re.compile(r'"version":\s*\((\d+)\D*(\d+)\D*(\d+)\)')
    with open(init_path, 'r') as f:
        whole_file = ''.join(f.readlines())
        version_match = version_reg.search(whole_file)
        if version_match:
            match_major, match_minor, match_patch = version_match.group(1), version_match.group(2), version_match.group(
                3)
            return match_major, match_minor, match_patch


def zip_main(addon_name):
    filename = generate_zip_filename(addon_name)
    lower_name = addon_name.lower()
    try:
        zipf = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
        zipdir('.', zipf, lower_name)
        zipf.close()
        print('Successfully created zip file: {}'.format(filename))
    except Exception as e:
        print('Failed to create {}: {}'.format(filename, e))
        exit(1)


if __name__ == '__main__':
    zip_main('nView-live')
