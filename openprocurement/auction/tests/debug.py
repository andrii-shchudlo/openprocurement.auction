import json
import contextlib
import os
import tempfile
import datetime
from dateutil.tz import tzlocal
from gevent.subprocess import check_output, sleep

PWD = os.path.dirname(os.path.realpath(__file__))
CWD = os.getcwd()

@contextlib.contextmanager
def update_auction_period():
    path = os.path.join("./src/openprocurement.auction/openprocurement/auction/tests/functional/data/tender_simple.json")
    with open(path) as file:
        data = json.loads(file.read())
    new_start_time = (datetime.datetime.now(tzlocal()) + datetime.timedelta(seconds=120)).isoformat()
    data['data']['auctionPeriod']['startDate'] = new_start_time
    with tempfile.NamedTemporaryFile(delete=False) as auction_file:
        json.dump(data, auction_file)
        auction_file.seek(0)
    yield auction_file.name
    auction_file.close()

def main():
  check_output('{0}/bin/circusd --daemon'.format(CWD).split())
  print "Circus is run..."
  print "Please wait..."
  with update_auction_period() as auction_file:
    check_output('{0}/bin/auction_worker planning {1}'
                 ' {0}/etc/auction_worker_dutch.yaml --planning_procerude partial_db --auction_info {2}'.format(CWD, "11111111111111111111111111111111", auction_file).split())
  sleep(10)
  print '='*100
  print u"To start the auction, enter the command"+"\n" \
        u" bin/auction_worker run 11111111111111111111111111111111 ./etc/auction_worker_defaults.yaml --planning_procerude partial_db --auction_info ./src/openprocurement.auction/openprocurement/auction/tests/functional/data/tender_simple.json"
  print '=' * 100

if __name__ == "__main__":
    main()
