import smtplib
import json

def send_email_test():
    data = {
        "receiverAddress": "justinyimcw@gmail.com",
        "course name": "comp3278",
        "venue": "cym",
        "time": "Fri 5:30",
    }
    send_email(data)


def send_email(data: dict):
    """
        data: json and dict type in python
        - format: {
            "receiverAddress": "",
            "course name": "comp3278",
            "venue": "cym",
            "time": "Fri 5:30",
            ... 
        }
    """ 
    receiverAddress = data["receiverAddress"]
    message = """
        \n
        ***Please dont reply. This is an automated email.*** \n
        There is a remainder for your following class:\n
    """
    
    for key, value in data.items():
        if key == "receiverAddress":
            pass
        else:
            if type(value) is not str:
                message += "\t" + key + ": " + str(value) + "\n"
            else:
                message += "\t" + key + ": " + value + "\n"
    
    toaddr = [receiverAddress]
    cc = [receiverAddress]
    bcc = [receiverAddress]

    toaddrs = toaddr + cc + bcc

    with smtplib.SMTP("smtp-mail.outlook.com", 587) as server:
        try:
            server.starttls()

            server.login("comp3278G20@outlook.com", "IloveDB3278")
            server.sendmail("comp3278G20@outlook.com", toaddrs, message)
            server.quit()
            return "Sent email success"
        except:
            print("Sent email unsuccess")

    return "Sent email unsuccess"

send_email_test()