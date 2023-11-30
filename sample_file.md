
# Title

Sample file content that you can write.
This is flexible to however you plan to get the data for the file content.
You can store file content in a database,
for example or if it's local you can read it in.

Example for how to read it in:

sample_file_path = "testing.py"

with open(sample_file_path, "r") as file:
    file_content = file.read()

You would then pass in file_content to github_repo.write_file_in_repo().
