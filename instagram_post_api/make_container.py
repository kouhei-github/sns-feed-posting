import json
import time
import requests

class InstagramAPI:
    def __init__(self, insta_business_id, access_token):
        self.insta_business_id = insta_business_id
        self.access_token = access_token
        self.post_url = f'https://graph.facebook.com/v17.0/{insta_business_id}/media?'

    def make_api_request(self, url, method, data):
        try:
            headers = {
                'Authorization': 'Bearer ' + self.access_token,
                'Content-Type': 'application/json',
            }
            options = {
                'headers': headers,
                'json': data,
                'timeout': 60,
            }
            response = requests.request(method, url, **options)
            response_data = response.json()
            print(response_data)
            if response.ok and 'id' in response_data:
                return int(response_data['id'])
            else:
                print(f'Instagram APIのリクエストでエラーが発生しました: {response_data}')
                return None
        except Exception as e:
            print('Instagram APIのリクエスト中にエラーが発生しました:', e)
            return None

    def wait_validation_container(self, container_ids):
        if isinstance(container_ids, int) or isinstance(container_ids, str):
            container_ids = [container_ids]
        for container_id in container_ids:
            url = f"https://graph.facebook.com/v17.0/{container_id}"
            while True:
                time.sleep(3)
                params = {
                    "fields": "status_code",
                    "access_token": self.access_token
                }
                r = requests.get(url, params=params)
                print(r.text)
                results = json.loads(r.text)
                if results.get('status_code') == "FINISHED":
                    break
                if results.get('status_code') == "ERROR":
                    break

    def make_image_container_api(self, media_url, caption='', location_id=None, user_tags=None, product_tags=None):
        data = {"image_url": media_url}
        if caption:
            data['caption'] = caption
        if location_id:
            data['location_id'] = location_id
        if user_tags:
            data['user_tags'] = user_tags
        if product_tags:
            data['product_tags'] = product_tags
        response_id = self.make_api_request(self.post_url, 'POST', data)
        if response_id:
            return {"media_type": "IMAGE", "creation_id": [response_id]}
        return None

    def make_reel_container_api(
        self, 
        media_url, 
        caption='', 
        share_to_feed=True, 
        collaborators=None, 
        cover_url=None, 
        user_tags=None, 
        location_id=None, 
        ):
        
        data = {"media_type": "REELS", "video_url": media_url}
        if caption:
            data['caption'] = caption
        if location_id:
            data['location_id'] = location_id
        if user_tags:
            data['user_tags'] = user_tags
        if share_to_feed:
            data['share_to_feed'] = share_to_feed
        if collaborators:
            data['collaborators'] = collaborators
        if cover_url:
            data['cover_url'] = cover_url
        response_id = self.make_api_request(self.post_url, 'POST', data)
        if response_id:
            return {"media_type": "REELS", "creation_id": [response_id]}
        return None

    def make_carousel_container_api(self, media_urls, caption='#BronzFonz'):
        contena_ids = []
        video = False
        at_least_one_video = False
        creation_id = None
        for media in media_urls:
            data = {'is_carousel_item': True}
            if media['type'] == 'IMAGE':
                data['image_url'] = media['media_url']
            else:
                data['video_url'] = media['media_url']
                data['media_type'] = 'REELS'
                video = True
                at_least_one_video = True
            if caption:
                data['caption'] = caption
            response_id = self.make_api_request(self.post_url, 'POST', data)
            if response_id:
                print("Conteneur OK")
                contena_ids.append(response_id)
                if video: creation_id = response_id
                video = False
        
        if contena_ids:
            payload = {"media_type": "CAROUSEL", "children": contena_ids}
            if at_least_one_video: self.wait_validation_container(creation_id)
            contena_group_id  = self.make_api_request(self.post_url, 'POST', payload)
            if contena_group_id :
                print("contena_group_id", contena_group_id  )
                return {'media_type': 'CAROUSEL', "creation_id": contena_group_id }
        return None

    def make_image_story_container_api(self, media_url):
        data = {"image_url": media_url}
        response_id = self.make_api_request(self.post_url, 'POST', data)
        if response_id:
            return {"media_type": "STORIES", "creation_id": [response_id]}
        return None
