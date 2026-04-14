import os
import shutil


def main():
    print("started")
    set_up_directory("static", "public")
    print("done")

def set_up_directory(source, destination):
    if not os.path.exists(source):
        raise Exception(f"Missing source argument: {source}")
    if os.path.exists(destination):
        shutil.rmtree(destination)
    shutil.copytree(source, destination)


if __name__ == "__main__":
    main()
