
from agenthub.hub.rest import Rest

HOST = 'localhost'
PORT = 443


class Dog:
    
    def bark(self, words):
        args = [words]
        url = '/agenthub/agent/xyz/call/Dog/bark/'
        body = {
            'request': {
                'args':[words]
            }
        }
        rest = Rest(HOST, PORT)
        return rest.post(url, body)


def main():
    dog = Dog()
    print dog.bark('My name is Doug')


if __name__ == '__main__':
    main()