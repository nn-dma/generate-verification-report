from datetime import datetime

# def format_pull_request_timestamp(dt_string: str) -> str:
#     # Remove precision
#     dt_string = dt_string.split(".")[0]
#     # Convert to datetime object
#     dt_object = datetime.strptime(dt_string, '%Y-%m-%dT%H:%M:%S')
#     # Rormat datetime object as string
#     formatted_string = dt_object.strftime('%Y-%m-%d %H:%M:%S')
#     # Print the formatted string
#     return formatted_string

def format_pull_request_timestamp(dt_string: str) -> str:
    # Remove precision
    dt_string = dt_string.split(".")[0]
    # Convert to datetime object
    dt_object = datetime.strptime(dt_string, '%Y-%m-%dT%H:%M:%S')
    # Format datetime object as string
    formatted_string = dt_object.strftime('%Y-%m-%d %H:%M:%S')
    # Print the formatted string
    return formatted_string

print(format_pull_request_timestamp("2023-05-16T09:22:18.5060551Z"))
