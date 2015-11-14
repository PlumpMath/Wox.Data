import os
import requests
import shutil

if __name__ == "__main__":
    url = "https://api.getwox.com/plugin/?page_size=100"
    base_url_for_file = "https://api.getwox.com/media/"
    r = requests.get(url, verify=False)
    data = r.json()
    for plugin in data['results']:
        name = plugin['name']
        username = plugin['created_by']['username']
        language = plugin['language'].lower()
        github = plugin['github']
        # e.g. plugin/D2D2C23B084D411DB66FE0C79D6C2A6D/Wox.Plugin.DoubanMovie-c0318e2c-0c2a-4c8c-a017-9d291b847d1d.wox
        plugin_file_name = plugin['plugin_file'].split('/')[2]
        plugin_file_url = "{}{}".format(base_url_for_file, plugin['plugin_file'])

        print("{}, {}, {}, {}, {}".format(name, username, language, github, plugin_file_name))
        if not os.path.exists(language):
            os.makedirs(language)
        plugin_downloaded = requests.get(plugin_file_url, verify=False, stream=True)
        plugin_file_path = os.path.join(language, plugin_file_name)
        if os.path.exists(plugin_file_path):
            os.remove(plugin_file_path)
        with open(plugin_file_path, 'wb') as f:
            shutil.copyfileobj(plugin_downloaded.raw, f)