import json
import subprocess
import sys

def main(token, defalut_repository):
    # GitHubのトークンを設定
    subprocess.run(f"gh auth login --with-token {token}", shell=True)
    
    # 対象リポジトリを取得
    with open("repositories.json", "r") as json_file:
        repositories = json.load(json_file)
        print(repositories)
    
    # 対象リポジトリのリリース情報を取得
    for repository in repositories:
        print(repositories[repository]['address'])
        address = repositories[repository]['address']
        output_json = subprocess.run(f"gh release list --repo {address}, --json createdAt,tagName", capture_output=True, text=True).stdout
        print(output_json)
        
if __name__=="__main__":
    token = sys.argv[1]
    defalut_repository = sys.argv[2]
    main(token=token, defalut_repository=defalut_repository)
        