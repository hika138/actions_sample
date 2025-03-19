import json
from pprint import pprint
import subprocess
import sys
import datetime
from pathlib import Path

def main(token, default_repository):
    # GitHubのトークンを設定
    subprocess.run(f"gh auth login --with-token {token}", shell=True)
    
    # 対象リポジトリを取得
    with open("repositories.json", "r") as json_file:
        repositories = json.load(json_file)

    # 対象リポジトリのリリース情報を取得し、更新があればissueを作成、更新
    try: 
        for repository in repositories:
            address = repositories[repository]['address']
            output = []
            
            # リリース情報を取得
            release_json = subprocess.run(f"gh release list --repo {address} --json createdAt,tagName", capture_output=True, text=True, shell=True).stdout
            print(release_json)
            release = json.loads(release_json)
            # 7日以内のリリース情報を取得
            for i in range(len(release)):
                if datetime.datetime.strptime(release[i]['createdAt'], '%Y-%m-%dT%H:%M:%SZ') > datetime.datetime.now() - datetime.timedelta(days=7):
                    output.append(release[i]['tagName'])
            if len(output) > 0:
                # issueを作成
                issue_title = f"{repository}: {(datetime.datetime.now() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')} ~ {datetime.datetime.now().strftime('%Y-%m-%d')}のリリース情報"
                with open(f"{repository}.md", "w") as f:
                    f.write("以下のリリースがあります。\n")
                    for i in range(len(output)):
                        f.write(f"[{output[i]}](https://github.com/nuxt/nuxt/releases/tag/{output[i]})\n")
                    
                subprocess.run(f'gh issue create --title "{issue_title}" --repo {default_repository} --body-file {repository}.md', shell=True)
    except Exception as e:
        print(e)
    
    finally:
        subprocess.run("ls -la", shell=True)
        print("終了")
        
if __name__=="__main__":
    token = sys.argv[1]
    default_repository = sys.argv[2]
    main(token=token, default_repository=default_repository)
        