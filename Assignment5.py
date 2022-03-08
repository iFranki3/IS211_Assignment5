import urllib.request
import csv


class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


class Server:
    def __init__(self):
        self.current_request = None
        self.time_remaining = 0

    def tick(self):
        if self.current_request != None:
            self.time_remaining = self.time_remaining - 1
        if self.time_remaining <= 0:
            self.current_request = None

    def busy(self):
        if self.current_request != None:
            return True
        else:
            return False

    def start_next(self, new_request):
        self.current_request = new_request
        self.time_remaining = new_request.get_process_time()


class Request:
    def __init__(self, time, process_time):
        self.timestamp = time
        self.process_time = process_time
        # self.pages = random.randrange(1, 21)

    def get_stamp(self):
        return self.timestamp

    def get_process_time(self):
        return self.process_time

    def wait_time(self, current_time):
        return current_time - self.timestamp


def simulateOneServer(file_url):
    response = urllib.request.urlopen(file_url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    cr = csv.reader(lines)
    request_list = []
    for row in cr:
        request_list.append((int(row[0]), int(row[2])))

    lab_server = Server()
    server_queue = Queue()
    waiting_times = []


    for current_second in range(21000):
        f_list = [y for (x, y) in request_list if x == current_second]
        for req_time in f_list:
            request = Request(current_second, req_time)
            server_queue.enqueue(request)

        if (not lab_server.busy()) and (not server_queue.is_empty()):
            next_request = server_queue.dequeue()
            waiting_times.append(next_request.wait_time(current_second))

            lab_server.start_next(next_request)
        lab_server.tick()

    average_wait = sum(waiting_times) / len(waiting_times)
    print("Average Wait %6.2f secs."
          % (average_wait))
def simulateManyServers(file_url,servers):
    response = urllib.request.urlopen(file_url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    cr = csv.reader(lines)
    request_list = []
    for row in cr:
        request_list.append((int(row[0]), int(row[2])))

    lab_server=[]
    for i in range(servers):
        a=Server()
        lab_server.append(a)
    server_queue = Queue()
    waiting_times = []

    for current_second in range(11000):
        f_list = [y for (x, y) in request_list if x == current_second]
        for req_time in f_list:
            request = Request(current_second, req_time)
            server_queue.enqueue(request)

        for server in lab_server:
            if (not server.busy()) and (not server_queue.is_empty()):
                next_request = server_queue.dequeue()
                waiting_times.append(next_request.wait_time(current_second))

                server.start_next(next_request)
            server.tick()

    average_wait = sum(waiting_times) / len(waiting_times)
    print("Average Wait %6.2f secs."
          % (average_wait))

def main(file_url,servers=1):
    if servers==1:
        simulateOneServer(file_url)
    else:
        simulateManyServers(file_url,servers)

if __name__ == "__main__":
    main('http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv')
    main('http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv',2)