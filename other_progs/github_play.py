import requests


def main():
    response = requests.get("https://api.github.com/users/devak23/repos")

    assert response.status_code == 200

    for repo in response.json():
        print ("[{}] {}".format(repo["language"], repo["name"]))

if __name__ == "__main__":
    main()