# key authentication is highly recommended for this script
import os
import shutil


def main():
    """
    Main function, creates and transfers file between remote machine and host 3 times.  Directory structure and remote machine
    name based off on my personal setup - may need to be changed

    Args:
    none

    Returns:
        none

    Raises:
        none

    """

    tempdir = "mkdir Tempdir"  # creates temporary directory for use in script
    transferdir = "scp -r /Users/johng/PycharmProjects/untitled1/Tempdir remote@remote:/home/remote/Projects"  # transfers temporary directory to pre-made directory on remote machine
    transferfile = "scp Tempdir/SuperSecretData.txt remote@remote:/home/remote/Projects/Tempdir"  # transfers text file SuperSecretData to Tempdir on remote host
    getfile = "scp remote@remote:/home/remote/Projects/Tempdir/SuperSecretData.txt /Users/johng/PycharmProjects/untitled1/Tempdir"  # retrieves SuperSecretData from remote host and adds it to Tempdir
    cleanup = "rm -r /Users/johng/PycharmProjects/untitled1/tempdir"  # removes Tempdir on local machine

    if not os.path.isdir("Tempdir"):
        os.system(tempdir)

    os.system(transferdir)

    file_check = os.path.join("Tempdir", "SuperSecretData.txt")

    if not os.path.exists(file_check):  # creates SuperSecretData.txt and moves it to Tempdir on local machine if it doesn't already exist
        with open("SuperSecretData.txt", 'wt') as file:
            file.write("Username:John Password: John")
        shutil.move("SuperSecretData.txt", "Tempdir")

    for x in range(3):  # sends and retrieves SuperSecretDirectory from local/remote machine 3 times
        os.system(transferfile)
        os.system(getfile)

    os.system(cleanup)


if __name__ == "__main__":
    main()
