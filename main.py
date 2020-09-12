import requests
import re
from subprocess import Popen, PIPE

BOT_TOKEN = "YOUR_BOT_TOKEN"
base_url = f"https://api.telegram.org/bot{BOT_TOKEN}"


# create func that get chat id
def get_chat_id(update):
    chat_id = update["message"]["chat"]["id"]
    return chat_id


# create func that get message text
def get_message_text(update):
    message_text = update["message"]["text"]
    return message_text


# create func that get last_update
def last_update(req):
    response = requests.get(req + "getUpdates")
    response = response.json()
    result = response["result"]
    total_updates = len(result) - 1
    return result[total_updates]


# create func that let bot send message to user
def send_message(chat_id, message_text):
    params = {"chat_id": chat_id, "text": message_text}
    response = requests.post(base_url + "sendMessage", data=params)
    return response


# create func that get dog picture
def get_dog_pic():
    allowed_extension = ['jpg', 'jpeg', 'png']
    file_extension = ''
    while file_extension not in allowed_extension:  # Get valid url for picture (jpg, jpeg, png)
        contents = requests.get('https://random.dog/woof.json').json()
        photo = contents['url']
        print(photo)
        file_extension = re.search("([^.]*)$", photo).group(1).lower()
    return photo


# create func that let bot send photo to user
def send_dog_photo(chat_id, photo_url):
    params = {"chat_id": chat_id, "photo": photo_url}
    response = requests.post(base_url + "sendPhoto", data=params)
    return response


# create func that get dog gif
def get_dog_gif():
    allowed_extension = ['mp4', 'gif']
    file_extension = ''
    while file_extension not in allowed_extension:  # Get valid url for gif (mp4, gif)
        contents = requests.get('https://random.dog/woof.json').json()
        gif = contents['url']
        print(gif)
        file_extension = re.search("([^.]*)$", gif).group(1).lower()
    return gif


# create func that let bot send gif to user
def send_dog_gif(chat_id, gif_url):
    params = {"chat_id": chat_id, "document": gif_url}
    response = requests.post(base_url + "sendDocument", data=params)
    return response


# create func that get link video of youtube
def get_links(link):
    # time.sleep(7)
    # link = get_message_text(update)
    cmd = "youtube-dl -g {}".format(link)
    r = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE).communicate()
    result = []
    res = r[0].split()
    for i in range(len(res)):
        result.append(res[i])
    return result


# create main func for navigate or reply message back
def main():
    update_id = last_update(req=base_url)["update_id"]
    while True:
        update = last_update(req=base_url)
        if update_id == update["update_id"]:
            if get_message_text(update).lower() == "hi" or get_message_text(
                    update) == "/start" or get_message_text(update).lower() == "hello":
                send_message(get_chat_id(update),
                             "Hello Welcome To My bot.\nCommands(#Fun)👇 \ndog: send photo of dog\ndog gif: send gif of dog\nAbout Command👇\nabout: information of me\n\n👉 and for get download link from youtube send youtube video link")

            elif get_message_text(update).lower() == "dog":
                send_dog_photo(get_chat_id(update), get_dog_pic())
                print(f"\033[33mDog Picture Sended. \nDog Picture Url -> {get_dog_pic()}\033[39m")

            elif get_message_text(update).lower() == "dog gif":
                send_dog_gif(get_chat_id(update), get_dog_gif())
                print(f"\033[33mDog Gif Sended. \nDog Gif Url -> {get_dog_gif()}\033[39m")

            elif "https://www.youtube.com" in get_message_text(
                    update).lower() or "http://www.youtube.com" in get_message_text(
                update) or "youtube.com" in get_message_text(update) or "m.youtube.com" in get_message_text(
                update) or "https://m.youtube.com" in get_message_text(
                update) or "http://m.youtube.com" in get_message_text(update):
                print(f"\033[33mYoutube Link -> {get_message_text(update)}\033[39m")
                links = get_links(get_message_text(update))
                send_message(get_chat_id(update), "video 👇\n{0}\nAudio 👇\n{1}".format(links[0], links[1]))
                print("\033[33mDownload Links Sended.\033[39m")

            elif get_message_text(update).lower() == "about":
                send_message(get_chat_id(update),
                        "#Author : Sullivan[Epic_R_R]\n#Email : salar.z@ourlook.de\n")

            else:
                send_message(get_chat_id(update), "Sorry Not Understand What You Inputted :(")
            update_id += 1


if __name__ == "__main__":
    print("\033[32mBot Starting\033[39m")
    main()
