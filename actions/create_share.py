import requests
from st2common.runners.base_action import Action

__all__ = [
    'CreateShareAction'
]

class CreateShareAction(Action):

    def run(self, commentary, title, url):

        access_token = self.config.get('access_token')

        resp = requests.get("https://api.linkedin.com/v2/me", headers = {
            "Authorization": "Bearer %s" % access_token
        })
        author_id = "urn:li:person:%s" % resp.json()['id']

        # https://docs.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/share-on-linkedin?context=linkedin/consumer/context
        resp = requests.post('https://api.linkedin.com/v2/ugcPosts', headers = {
            "Authorization": "Bearer %s" % access_token,
            "Content-Type": "text/plain"
        }, json = {
            "author": author_id,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": commentary
                    },
                    "shareMediaCategory": "ARTICLE",
                    "media": [
                        {
                            "status": "READY",
                            "originalUrl": url,
                            "title": {
                                "text": title
                            }
                        }
                    ]
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        })

        if resp.update_status == 201:
            return (True, resp.json()['id'])
        else:
            return (False, None)
