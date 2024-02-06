import json
import requests
import base64
from datetime import datetime
import re
import sys
import os

# EXAMPLE RESPONSE:

# response = '''
# {
#     "queries": [
#         {
#             "type": "commit",
#             "items": [
#                 "c28d6e0e5d93c6f211ea4b16860a7847924fc0ff"
#             ]
#         }
#     ],
#     "results": [
#         {
#             "c28d6e0e5d93c6f211ea4b16860a7847924fc0ff": [
#                 {
#                     "repository": {
#                         "id": "353c8fbd-3138-4aca-bad6-d89b4a2e1bb9",
#                         "url": "https://dev.azure.com/novonordiskit/0f8910bf-8ddd-40e8-a349-4e4d6c3a5221/_apis/git/repositories/353c8fbd-3138-4aca-bad6-d89b4a2e1bb9"
#                     },
#                     "pullRequestId": 77166,
#                     "codeReviewId": 77166,
#                     "status": "completed",
#                     "createdBy": {
#                         "displayName": "Lasse Lund Sten Jensen",
#                         "url": "https://spsprodweu1.vssps.visualstudio.com/A0621c93c-2aaf-4833-93ab-f4aaea37cdae/_apis/Identities/c09252a3-b821-64ea-b769-67a8ba293287",
#                         "_links": {
#                             "avatar": {
#                                 "href": "https://dev.azure.com/novonordiskit/_apis/GraphProfile/MemberAvatars/aad.YzA5MjUyYTMtYjgyMS03NGVhLWI3NjktNjdhOGJhMjkzMjg3"
#                             }
#                         },
#                         "id": "c09252a3-b821-64ea-b769-67a8ba293287",
#                         "uniqueName": "LLZJ@novonordisk.com",
#                         "imageUrl": "https://dev.azure.com/novonordiskit/_api/_common/identityImage?id=c09252a3-b821-64ea-b769-67a8ba293287",
#                         "descriptor": "aad.YzA5MjUyYTMtYjgyMS03NGVhLWI3NjktNjdhOGJhMjkzMjg3"
#                     },
#                     "creationDate": "2023-02-07T14:36:03.0415887Z",
#                     "closedDate": "2023-02-07T14:36:29.9788557Z",
#                     "title": "Release 0.1.46 of service1",
#                     "description": "Release 0.1.46 of service1",
#                     "sourceRefName": "refs/heads/main",
#                     "targetRefName": "refs/heads/release/service1",
#                     "mergeStatus": "succeeded",
#                     "isDraft": false,
#                     "mergeId": "7cc1fc9a-606e-4fdd-80f6-fbb3cf574349",
#                     "lastMergeSourceCommit": {
#                         "commitId": "553e0ac8db0b0319367041c9d06d5f24118a4461",
#                         "url": "https://dev.azure.com/novonordiskit/0f8910bf-8ddd-40e8-a349-4e4d6c3a5221/_apis/git/repositories/353c8fbd-3138-4aca-bad6-d89b4a2e1bb9/commits/553e0ac8db0b0319367041c9d06d5f24118a4461"
#                     },
#                     "lastMergeTargetCommit": {
#                         "commitId": "a6abf76a10dc8e77075418ef8899f7b6afd29fbc",
#                         "url": "https://dev.azure.com/novonordiskit/0f8910bf-8ddd-40e8-a349-4e4d6c3a5221/_apis/git/repositories/353c8fbd-3138-4aca-bad6-d89b4a2e1bb9/commits/a6abf76a10dc8e77075418ef8899f7b6afd29fbc"
#                     },
#                     "lastMergeCommit": {
#                         "commitId": "cecfec64e6d4dc33556d289cfa3db355e7c01206",
#                         "url": "https://dev.azure.com/novonordiskit/0f8910bf-8ddd-40e8-a349-4e4d6c3a5221/_apis/git/repositories/353c8fbd-3138-4aca-bad6-d89b4a2e1bb9/commits/cecfec64e6d4dc33556d289cfa3db355e7c01206"
#                     },
#                     "url": "https://dev.azure.com/novonordiskit/0f8910bf-8ddd-40e8-a349-4e4d6c3a5221/_apis/git/repositories/353c8fbd-3138-4aca-bad6-d89b4a2e1bb9/pullRequests/77166",
#                     "completionOptions": {
#                         "mergeCommitMessage": "Merged PR 77166: Release 0.1.46 of service1\n\nRelease 0.1.46 of service1",
#                         "mergeStrategy": "noFastForward",
#                         "transitionWorkItems": true,
#                         "autoCompleteIgnoreConfigIds": []
#                     },
#                     "supportsIterations": true,
#                     "completionQueueTime": "2023-02-07T14:36:28.9546641Z"
#                 }
#             ]
#         }
#     ]
# }'''


work_item_list = []


def link_work_item(work_item, auth_method, access_token, organization):

    url = f"https://dev.azure.com/{organization}/_apis/wit/workitems/{work_item}?api-version=7.0"

    payload = [
        {
            "op": "add",
            "path": "/relations/-",
            "value": {
                "rel": "ArtifactLink",
                "url": f"vstfs:///Build/Build/{os.getenv('BUILD_ID')}",
                "attributes": {
                    "comment": "Making a new link for the build",
                    "name": "Build",
                },
            },
        }
    ]

    print(payload)

    headers = {
        "Content-Type": "application/json-patch+json",
        "Authorization": f"{auth_method} {access_token}",
    }

    response = requests.request("PATCH", url, headers=headers, json=payload)

    print(response.text)


# TODO: Add exception handling
def get_pull_request(
    commit_hash, auth_method, access_token, organization, project, repository
):
    # Replace with the right organization id, project id and repository id
    # url = "https://dev.azure.com/novonordiskit/Data%20Management%20and%20Analytics/_apis/git/repositories/QMS-TEMPLATE/pullrequestquery?api-version=7.0"
    url = f"https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{repository}/pullrequestquery?api-version=7.0"

    payload = json.dumps(
        {"queries": [{"items": [f"{commit_hash}"], "type": "lastMergeCommit"}]}
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"{auth_method} {access_token}",
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text


def get_work_items_link(
    commit_hash, auth_method, access_token, organization, project, repository, work_item
):
    # Replace with the right organization id, project id and work item id
    # url = "https://dev.azure.com/novonordiskit/Data%20Management%20and%20Analytics/_apis/git/repositories/QMS-TEMPLATE/pullrequestquery?api-version=7.0"
    url = f"https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{work_item}?api-version=7.0"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"{auth_method} {access_token}",
    }

    response = requests.request("GET", url, headers=headers)
    r = json.loads(response.text, strict=False)
    work_item_list.append(r["_links"]["html"]["href"])


# TODO: Add exception handling
def get_pull_request_id(response, commit_hash):
    r = json.loads(response, strict=False)
    pull_request = r["results"][0][commit_hash][0]
    # url = pull_request['url']
    mergeCommitMessage = pull_request["completionOptions"]["mergeCommitMessage"]
    # workItem = re.search("132", mergeCommitMessage).group()
    pull_request_id = pull_request["pullRequestId"]
    return pull_request_id


def get_work_items(response, commit_hash):
    r = json.loads(response, strict=False)
    pull_request = r["results"][0][commit_hash][0]
    mergeCommitMessage = pull_request["completionOptions"]["mergeCommitMessage"]
    workItems = re.findall(r"#(\d+)", mergeCommitMessage)
    return workItems


# TODO: Add exception handling
def get_pull_request_closed_timestamp(response, commit_hash):
    r = json.loads(response, strict=False)
    pull_request = r["results"][0][commit_hash][0]
    pull_request_closed_timestamp = pull_request["closedDate"]
    return pull_request_closed_timestamp

def format_pull_request_timestamp(dt_string: str) -> str:
    # Remove precision
    # NOTE: This is done because Python .strptime supports 6 digit precision on datetime strings, but the one we get from Azure DevOps has 7 digits
    dt_string = dt_string.split(".")[0]
    # Convert to datetime object
    dt_object = datetime.strptime(dt_string, '%Y-%m-%dT%H:%M:%S')
    # Format datetime object as string
    formatted_string = dt_object.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_string

# TODO: Add exception handling
def main(argv):
    # 1. Check for the arg pattern (NOTE: don't bother checking——the below access token is a randomized example):
    #   python3 get_pull_request_id.py -commit 928e54d9021d1350e4b58a4426a9c85de766e5a2 -accesstoken KmUzxHc1YTZpdHh3Nk6JJ7gf3TZkb3N5eGo0ZDM3Z3dhhcJ3s2NnYjJsN3phcb1waWE= -organization novonordiskit -project Data%20Management%20and%20Analytics -repository QMS-TEMPLATE -result pull_request_id
    #   e.g. argv[0] is '-commit'
    #        argv[1] is '928e54d9021d1350e4b58a4426a9c85de766e5a2'
    #        argv[2] is '-accesstoken'
    #        argv[3] is 'KmUzxHc1YTZpdHh3Nk6JJ7gf3TZkb3N5eGo0ZDM3Z3dhhcJ3s2NnYjJsN3phcb1waWE='
    #        argv[4] is '-organization'
    #        argv[5] is 'novonordiskit'
    #        argv[6] is '-project'
    #        argv[7] is 'Data Management and Analytics'
    #        argv[8] is '-repository'
    #        argv[9] is 'QMS-TEMPLATE'
    #        argv[10] is '-result'
    #        argv[11] is 'pull_request_id' OR 'pull_request_closed_timestamp'
    if (
        len(argv) == 12
        and argv[0] == "-commit"
        and argv[2] == "-accesstoken"
        and argv[4] == "-organization"
        and argv[6] == "-project"
        and argv[8] == "-repository"
        and argv[10] == "-result"
    ):
        # Create rendering for the test result
        commit_hash = argv[1]
        access_token = argv[3]
        organization = argv[5]
        project = argv[7]
        repository = argv[9]
        result = argv[11]

        # URL encode the project name
        project = project.replace(" ", "%20")

        # Use environment variable to read the protected access token if we are running in Azure DevOps
        auth_method = "Basic"
        if access_token == "USE_ENV_VARIABLE":
            access_token = os.environ["SYSTEM_ACCESSTOKEN"]
            auth_method = "Bearer"
        # If auth method is "Basic", we are most likely running outside Azure DevOps, so we need to encode the 
        # access token as password in a Basic HTTP Auth header format
        if auth_method == "Basic":
            # Base64 encode userid:password, which is empty (no user id) and the access_token value in a string "<user_id>:<access_token>", e.g. ":dkjhsDhjksd289712984Fdjhksd".
            access_token = base64.b64encode(f":{access_token}".encode()).decode()

        response = get_pull_request(
            commit_hash, auth_method, access_token, organization, project, repository
        )
        
        pull_request_id = get_pull_request_id(response, commit_hash)
        work_items = get_work_items(response, commit_hash)
        pull_request_closed_timestamp = get_pull_request_closed_timestamp(
            response, commit_hash
        )

        if result == "pull_request_id":
            print(pull_request_id)
        elif result == "pull_request_closed_timestamp":
            print(format_pull_request_timestamp(pull_request_closed_timestamp))
        elif result == "work_items":
            [
                get_work_items_link(
                    commit_hash,
                    auth_method,
                    access_token,
                    organization,
                    project,
                    repository,
                    work_item,
                )
                for work_item in work_items
            ]
            if len(work_item_list) == 0:
                print(f"<kbd>!MISSING!</kbd>")
            for work_item_link in work_item_list:
                print(
                    f"<kbd><a href=\"{work_item_link}\">{work_item_link.rsplit('/',1)[1]}</a></kbd>"
                )
        elif result == "add_work_item_link":

            [
                link_work_item(
                    work_item_id,
                    auth_method,
                    access_token,
                    organization,
                )
                for work_item_id in work_items
            ]
        else:
            print("Invalid result argument")


if __name__ == "__main__":
    main(sys.argv[1:])
