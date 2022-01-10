import subprocess


def show_notification(title_message="title", body_message="message"):
    subprocess.Popen(["notify-send", title_message, body_message], stdout=subprocess.PIPE, universal_newlines=True)

# show_notification()
