import sys
import glob
import os
import subprocess


def extract_configuration_specification_tags(lines):
    tags = []
    readTags = False
    for i, line in enumerate(lines):
        if 'tags:' in line:
            # tags:
            readTags = True
        if readTags:
            #   - service_now_integration
            if '- ' in line:
                tags.append(line.split('- ')[1].strip())
            if '---' in line: # This marks the end of a tag section, so do not process the rest of the file.
                # ---
                break
    return tags

def extract_last_modified_commit_hash(filepath, branch):
    # git log <remote branch> -n 1 --pretty=format:%H -- <filepath>
    result = subprocess.run(['git', 'log', branch, '-n', '1', '--pretty=format:%H', '--', filepath], stdout=subprocess.PIPE)
    return result.stdout.decode()

def extract_last_modified_commit_hash_timestamp(commit_hash):
    # git show -s --format=%cd --date=format:'%Y-%m-%d %H:%M:%S' <commit_hash>
    result = subprocess.run(['git', 'show', '-s', '--format=%cd', "--date=format:'%Y-%m-%d %H:%M:%S'", commit_hash], stdout=subprocess.PIPE)
    return result.stdout.decode()

# TODO: Add exception handling
def main(argv):
    # Guard clause, no arguments provided
    if len(argv) == 0:
        print("No arguments provided")
        exit(1)
    # Guard clause, too few arguments provided
    if len(argv) < 10:
        print("Not all required arguments provided")
        exit(1)

    # 2. Check for the arg pattern:
    #   python3 render_configuration_specifications.py -folder <filepath> -branch <remote branch> -organization <organization> -project <project> -repository <repository>
    #   e.g. 
    #       argv[0] is '-folder'
    #       argv[1] is './system_documentation/docs/configuration'
    #       argv[2] is '-branch'
    #       argv[3] is 'origin/release/service1'
    #       argv[4] is '-organization'
    #       argv[5] is 'novonordiskit'
    #       argv[6] is '-project'
    #       argv[7] is 'Data Management and Analytics'
    #       argv[8] is '-repository'
    #       argv[9] is 'QMS-TEMPLATE'
    if len(argv) == 10 and argv[0] == '-folder' and argv[2] == '-branch' and argv[4] == '-organization' and argv[6] == '-project' and argv[8] == '-repository':
        # Render all configuration specifications
        # Find all .md files in the folder and subfolders
        path = r'%s/**/*.md' % argv[1]
        files = glob.glob(path, recursive=True)

        # Get the current branch
        branch = argv[3]
        organization = argv[5]
        project = argv[7]
        repository = argv[9]

        # URL encode the project name
        project = project.replace(" ", "%20")
        
        # Render the table header and the table body element
        print('''<figure>
    <table>
        <thead>
            <tr>
                <th scope="col">#</th>
                <th scope="col">Configuration specification</th>
                <th scope="col">Version</th>
                <th scope="col">Last modified</th>
                <th scope="col">Trace to requirements</th>
            </tr>
        </thead>
        <tbody>''')

        count_configuration_specifications = 0
        for file in files:
            #print(f"File: {file}")
            last_modified_commit_hash = extract_last_modified_commit_hash(file, branch)
            last_modified_commit_hash_timestamp = extract_last_modified_commit_hash_timestamp(last_modified_commit_hash).strip().replace("'", "")

            with open(file, mode='r', encoding='utf-8') as file_reader:
                lines = file_reader.read().split('\n')
                configuration_specification_tags = extract_configuration_specification_tags(lines)
                # Extract the path to the markdown file, e.g.:
                # /system_documentation/docs/configuration/AzureAD/index.md
                repository_file_path = os.path.abspath(file).replace(os.getcwd(), "")
                # Create link to path for file, e.g.:
                # https://dev.azure.com/novonordiskit/Data%20Management%20and%20Analytics/_git/QMS-TEMPLATE/commit/d78d1bf6bd41b07f654c6b8178fb85b4490853f3?path=/system_documentation/docs/configuration/AzureAD/index.md
                repository_file_link = f'https://dev.azure.com/{organization}/{project}/_git/{repository}/commit/{last_modified_commit_hash}?path={repository_file_path}'

                count_configuration_specifications += 1
                print(f'''            <tr>
                <th scope="row">{count_configuration_specifications}</th>
                <td><a href="{repository_file_link}" target="_blank">{repository_file_path}</a></td>
                <td>{last_modified_commit_hash}</td>
                <td>{last_modified_commit_hash_timestamp}</td>
                <td>{ '<kbd>' + '</kbd><kbd>'.join(configuration_specification_tags) + '</kbd>' if configuration_specification_tags else 'N/A' }</td>
            </tr>''')

        # Render the table body close elements
        print('''        </tbody>
    </table>
</figure>''')

if __name__ == "__main__":
   main(sys.argv[1:])