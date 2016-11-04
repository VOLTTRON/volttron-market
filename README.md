# README #

This repository contains VOLTTRON agents and classes useful for simulating double-auction markets. Typically, the Buyer, Seller and Middleman agents would not be run on the VOLTTRON platform as provided, but instead would be installed into the VOLTTRON virtual environment and extended by agents requiring this functionality. This README contains instructions for installing these modules into the VOLTTRON virtual environments' site-packages directory.

## DEPENDENCIES ##

The following instructions assume you have already cloned this repository, and that you have already installed the [PubSub](https://github.com/VOLTTRON/volttron-pubsub) modules into the VOLTTRON environment's site-packages directory. To run the plotter agent included in the example you must install the matplotlib module in the VOLLTRON virtual environment, or preferably, put an existing installation of the module on your Python path. The TkAgg backend is needed.

Make sure you have installed [VOLTTRON](https://github.com/VOLTTRON/volttron) and its dependencies.

## INSTALLATION ##

Enable the VOLTTRON virtual environment
~~~
$ . [VOLTTRON repository location]/env/bin/activate
~~~
Install the package.
~~~
$ cd [volttron-market repository location]
$ python setup.py install
~~~

## AGENT CONFIGURATION FOR EXAMPLE 1 ##

No changes need to be made for the included example.

## PACKAGING AND RUNNING EXAMPLE 1 ##

Navigate to VOLTTRON source directory
~~~
$ cd [VOLTTRON repository location]
~~~
Enable the VOLTTRON virtual environment (if not already enabled).
~~~
$ . env/bin/activate
~~~
Run VOLTTRON
~~~
$ volttron -vv -l [logfilepath.log] &
~~~
Export environment variables required for make-agent.sh
~~~
$ export SOURCE=../volttron-market/pnnl/plotteragent/
$ export CONFIG=../volttron-market/config/plotter
$ export TAG=plotter
$ . scripts/core/make-agent.sh
$ export SOURCE=../volttron-market/pnnl/buyeragent/
$ export CONFIG=../volttron-market/config/air-buyer
$ export TAG=air-buyer
$ . scripts/core/make-agent.sh
$ export SOURCE=../volttron-market/pnnl/marketagent/
$ export CONFIG=../volttron-market/config/air-market
$ export TAG=air-market
$ . scripts/core/make-agent.sh
$ export SOURCE=../volttron-market/pnnl/selleragent/
$ export CONFIG=../volttron-market/config/air-seller
$ export TAG=air-seller
$ . scripts/core/make-agent.sh
$ export SOURCE=../volttron-market/pnnl/directoragent/
$ export CONFIG=../volttron-market/config/director
$ export TAG=director
$ . scripts/core/make-agent.sh
~~~
View the log. You will observe the agents log the messages sent back and forth during the market simulation.
~~~
$ tail -f [logfilepath.log]
...
2016-09-29 10:22:00,724 (director-0.1 7616) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/collectreservations/request [{'collectReservations': True}, {}]
2016-09-29 10:22:00,727 (market-0.1 7386) market.agent INFO: Received collect reservations request
2016-09-29 10:22:00,727 (market-0.1 7386) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/air/reservation/request [{'commodity': 'air'}, {}]
2016-09-29 10:22:00,730 (buyer-0.1 7271) buyer.agent INFO: Received: test/air/reservation/request {'commodity': 'air'}
2016-09-29 10:22:00,730 (buyer-0.1 7271) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/air/reservation/response [{'curve': None, 'type': 'BUY', 'commodity': 'air'}, {}]
2016-09-29 10:22:00,731 (seller-0.1 7501) seller.agent INFO: Received: test/air/reservation/request {'commodity': 'air'}
2016-09-29 10:22:00,732 (seller-0.1 7501) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/air/reservation/response [{'curve': None, 'type': 'SELL', 'commodity': 'air'}, {}]
2016-09-29 10:22:00,738 (market-0.1 7386) market.agent INFO: Received Reservation: e74dcd7a-59b9-467b-8f8d-c2cbec718cf2 {'curve': None, 'type': 'BUY', 'commodity': 'air'}
2016-09-29 10:22:00,738 (market-0.1 7386) market.agent INFO: Received Reservation: 05a1a068-c49b-4e8c-aa55-0f3e94c03da4 {'curve': None, 'type': 'SELL', 'commodity': 'air'}
2016-09-29 10:22:02,727 (director-0.1 7616) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/collectoffers/request [{'collectOffers': True}, {}]
2016-09-29 10:22:02,732 (market-0.1 7386) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/air/offer/request [{'commodity': 'air'}, {}]
2016-09-29 10:22:02,740 (buyer-0.1 7271) buyer.agent INFO: Received: test/air/offer/request {'commodity': 'air'}
2016-09-29 10:22:02,740 (buyer-0.1 7271) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/air/offer/response [{'curve': [(0.0, 100.0), (100.0, 0.0)], 'type': 'BUY', 'commodity': 'air'}, {}]
2016-09-29 10:22:02,745 (seller-0.1 7501) seller.agent INFO: Received: test/air/offer/request {'commodity': 'air'}
2016-09-29 10:22:02,745 (seller-0.1 7501) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/air/offer/response [{'curve': [(0.0, 0.0), (100.0, 100.0)], 'type': 'SELL', 'commodity': 'air'}, {}]
2016-09-29 10:22:02,759 (market-0.1 7386) <stdout> INFO: AirMarket does not have enough SELL offers.
2016-09-29 10:22:02,759 (market-0.1 7386) <stdout> INFO: AirMarket has enough BUY and SELL offers.
2016-09-29 10:22:02,751 (market-0.1 7386) market.agent INFO: Received Offer: e74dcd7a-59b9-467b-8f8d-c2cbec718cf2 {'curve': [[0.0, 100.0], [100.0, 0.0]], 'type': 'BUY', 'commodity': 'air'}
2016-09-29 10:22:02,755 (market-0.1 7386) market.agent INFO: Received Offer: 05a1a068-c49b-4e8c-aa55-0f3e94c03da4 {'curve': [[0.0, 0.0], [100.0, 100.0]], 'type': 'SELL', 'commodity': 'air'}
2016-09-29 10:22:02,769 (market-0.1 7386) <stdout> INFO: AirMarket clears air at 50.0
2016-09-29 10:22:04,738 (director-0.1 7616) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/clear/request [{'clear': True}, {}]
2016-09-29 10:22:04,742 (market-0.1 7386) market.agent INFO: Received clear request from dd88dc81-670d-46ed-802f-ae2b2be6584e
2016-09-29 10:22:04,742 (market-0.1 7386) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/air/clear/request [{'price': 50.00000000000006, 'commodity': 'air', 'quantity': 50.00000000000006}, {}]
2016-09-29 10:22:04,746 (seller-0.1 7501) pnnl.pubsubagent.pubsub.agent INFO: Received: test/air/clear/request [{'price': 50.00000000000006, 'commodity': 'air', 'quantity': 50.00000000000006}, {}]
...
~~~

The market will be cleared every 5 seconds until the agents are stopped.

## AGENT CONFIGURATION FOR EXAMPLE 2 ##

No changes need to be made for the included example.

## PACKAGING AND RUNNING EXAMPLE 2 ##

Navigate to VOLTTRON source directory
~~~
$ cd [VOLTTRON repository location]
~~~
Enable the VOLTTRON virtual environment (if not already enabled).
~~~
$ . env/bin/activate
~~~
Run VOLTTRON
~~~
$ volttron -vv -l [logfilepath.log] &
~~~
Export environment variables required for make-agent.sh
~~~
$ export SOURCE=../volttron-market/pnnl/plotteragent/
$ export CONFIG=../volttron-market/config/plotter
$ export TAG=plotter
$ . scripts/core/make-agent.sh
$ export SOURCE=../volttron-market/pnnl/buyeragent/
$ export CONFIG=../volttron-market/config/air-buyer
$ export TAG=air-buyer
$ . scripts/core/make-agent.sh
$ export SOURCE=../volttron-market/pnnl/marketagent/
$ export CONFIG=../volttron-market/config/air-market
$ export TAG=air-market
$ . scripts/core/make-agent.sh
$ export SOURCE=../volttron-market/pnnl/middlemanagent/
$ export CONFIG=../volttron-market/config/middleman
$ export TAG=middleman
$ . scripts/core/make-agent.sh
$ export SOURCE=../volttron-market/pnnl/marketagent/
$ export CONFIG=../volttron-market/config/electricity-market
$ export TAG=electricity-market
$ . scripts/core/make-agent.sh
$ export SOURCE=../volttron-market/pnnl/selleragent/
$ export CONFIG=../volttron-market/config/electricity-seller
$ export TAG=electricity-seller
$ . scripts/core/make-agent.sh
$ export SOURCE=../volttron-market/pnnl/directoragent/
$ export CONFIG=../volttron-market/config/director
$ export TAG=director
$ . scripts/core/make-agent.sh
~~~
~~~
View the log. You will observe the agents log the messages sent back and forth during the market simulation.
~~~
$ tail -f [logfilepath.log]
~~~
~~~
...
2016-09-29 10:14:32,923 (director-0.1 6353) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/collectreservations/request [{'collectReservations': True}, {}]
2016-09-29 10:14:32,936 (seller-0.1 6238) seller.agent INFO: Received: test/electricity/reservation/request {'commodity': 'electricity'}
2016-09-29 10:14:32,936 (seller-0.1 6238) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/electricity/reservation/response [{'curve': None, 'type': 'SELL', 'commodity': 'electricity'}, {}]
2016-09-29 10:14:32,932 (buyer-0.1 5776) buyer.agent INFO: Received: test/air/reservation/request {'commodity': 'air'}
2016-09-29 10:14:32,932 (buyer-0.1 5776) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/air/reservation/response [{'curve': None, 'type': 'BUY', 'commodity': 'air'}, {}]
2016-09-29 10:14:32,930 (middleman-0.1 6006) middleman.agent INFO: Received Sell Reservation Request: test/air/reservation/request {'commodity': 'air'}
2016-09-29 10:14:32,930 (middleman-0.1 6006) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/air/reservation/response [{'curve': None, 'type': 'SELL', 'commodity': 'air'}, {}]
2016-09-29 10:14:32,938 (middleman-0.1 6006) middleman.agent INFO: Received Buy Reservation Request: test/electricity/reservation/request {'commodity': 'electricity'}
2016-09-29 10:14:32,938 (middleman-0.1 6006) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/electricity/reservation/response [{'curve': None, 'type': 'BUY', 'commodity': 'electricity'}, {}]
2016-09-29 10:14:32,928 (market-0.1 6123) market.agent INFO: Received collect reservations request
2016-09-29 10:14:32,929 (market-0.1 6123) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/electricity/reservation/request [{'commodity': 'electricity'}, {}]
2016-09-29 10:14:32,927 (market-0.1 5891) market.agent INFO: Received collect reservations request
2016-09-29 10:14:32,927 (market-0.1 5891) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/air/reservation/request [{'commodity': 'air'}, {}]
2016-09-29 10:14:32,939 (market-0.1 5891) market.agent INFO: Received Reservation: 290ec7a5-fd8f-486f-980b-9fc2fcb04db6 {'curve': None, 'type': 'SELL', 'commodity': 'air'}
2016-09-29 10:14:32,939 (market-0.1 5891) market.agent INFO: Received Reservation: 11cdac8e-2bc0-4504-87f8-af40724aac7b {'curve': None, 'type': 'BUY', 'commodity': 'air'}
2016-09-29 10:14:32,948 (market-0.1 6123) market.agent INFO: Received Reservation: abd22ce4-c0b6-4f5c-a694-bbde745f8b48 {'curve': None, 'type': 'SELL', 'commodity': 'electricity'}
2016-09-29 10:14:32,950 (market-0.1 6123) market.agent INFO: Received Reservation: 290ec7a5-fd8f-486f-980b-9fc2fcb04db6 {'curve': None, 'type': 'BUY', 'commodity': 'electricity'}
2016-09-29 10:14:34,931 (director-0.1 6353) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/collectoffers/request [{'collectOffers': True}, {}]
2016-09-29 10:14:34,978 (market-0.1 6123) <stdout> INFO: ElectricityMarket does not have enough BUY offers.
2016-09-29 10:14:34,954 (buyer-0.1 5776) buyer.agent INFO: Received: test/air/offer/request {'commodity': 'air'}
2016-09-29 10:14:34,955 (buyer-0.1 5776) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/air/offer/response [{'curve': [(0.0, 100.0), (100.0, 0.0)], 'type': 'BUY', 'commodity': 'air'}, {}]
2016-09-29 10:14:34,947 (seller-0.1 6238) seller.agent INFO: Received: test/electricity/offer/request {'commodity': 'electricity'}
2016-09-29 10:14:34,948 (seller-0.1 6238) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/electricity/offer/response [{'curve': [(0.0, 0.0), (100.0, 100.0)], 'type': 'SELL', 'commodity': 'electricity'}, {}]
2016-09-29 10:14:34,940 (middleman-0.1 6006) middleman.agent INFO: Received Buy Bid Request: test/electricity/offer/request {'commodity': 'electricity'}
2016-09-29 10:14:34,940 (middleman-0.1 6006) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/air/demandcurve/request [{'commodity': 'air'}, {}]
2016-09-29 10:14:34,954 (middleman-0.1 6006) middleman.agent INFO: Received Sell Bid Request: test/air/offer/request {'commodity': 'air'}
2016-09-29 10:14:34,935 (market-0.1 5891) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/air/offer/request [{'commodity': 'air'}, {}]
2016-09-29 10:14:34,963 (market-0.1 5891) market.agent INFO: Received request for demand curve from : 290ec7a5-fd8f-486f-980b-9fc2fcb04db6 {'commodity': 'air'}
2016-09-29 10:14:34,978 (market-0.1 5891) market.agent INFO: Received Offer: 11cdac8e-2bc0-4504-87f8-af40724aac7b {'curve': [[0.0, 100.0], [100.0, 0.0]], 'type': 'BUY', 'commodity': 'air'}
2016-09-29 10:14:34,979 (market-0.1 5891) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/air/demandcurve/response [{'curve': [(0.0, 100.0), (1.0101010101010104, 98.98989898989899), (2.0202020202020208, 97.97979797979798), (3.030303030303031, 96.96969696969697), (4.040404040404027, 95.95959595959597), (5.050505050505038, 94.94949494949496), (6.060606060606048, 93.93939393939395), (7.0707070707070585, 92.92929292929294), (8.080808080808069, 91.91919191919193), (9.09090909090908, 90.90909090909092), (10.10101010101009, 89.89898989898991), (11.1111111111111, 88.8888888888889), (12.12121212121211, 87.87878787878789), (13.13131313131312, 86.86868686868688), (14.141414141414131, 85.85858585858587), (15.151515151515142, 84.84848484848486), (16.161616161616152, 83.83838383838385), (17.171717171717162, 82.82828282828284), (18.181818181818173, 81.81818181818183), (19.191919191919183, 80.80808080808082), (20.202020202020194, 79.7979797979798), (21.212121212121204, 78.7878787878788), (22.222222222222214, 77.77777777777779), (23.232323232323225, 76.76767676767678), (24.242424242424235, 75.75757575757576), (25.252525252525245, 74.74747474747475), (26.262626262626256, 73.73737373737374), (27.272727272727266, 72.72727272727273), (28.282828282828277, 71.71717171717172), (29.292929292929287, 70.70707070707071), (30.303030303030297, 69.6969696969697), (31.313131313131308, 68.68686868686869), (32.32323232323232, 67.67676767676768), (33.33333333333333, 66.66666666666667), (34.34343434343434, 65.65656565656566), (35.35353535353535, 64.64646464646465), (36.36363636363636, 63.63636363636364), (37.37373737373737, 62.62626262626263), (38.38383838383838, 61.61616161616162), (39.39393939393939, 60.60606060606061), (40.4040404040404, 59.5959595959596), (41.41414141414141, 58.58585858585859), (42.42424242424242, 57.57575757575758), (43.43434343434343, 56.56565656565657), (44.44444444444444, 55.55555555555556), (45.45454545454545, 54.54545454545455), (46.464646464646464, 53.535353535353536), (47.474747474747474, 52.525252525252526), (48.484848484848484, 51.515151515151516), (49.494949494949495, 50.505050505050505), (50.505050505050505, 49.494949494949495), (51.515151515151516, 48.484848484848484), (52.52525252525252, 47.47474747474748), (53.53535353535353, 46.46464646464647), (54.54545454545454, 45.45454545454546), (55.55555555555555, 44.44444444444445), (56.56565656565656, 43.43434343434344), (57.57575757575757, 42.42424242424243), (58.58585858585858, 41.41414141414142), (59.59595959595959, 40.40404040404041), (60.6060606060606, 39.3939393939394), (61.61616161616161, 38.38383838383839), (62.62626262626262, 37.37373737373738), (63.63636363636363, 36.36363636363637), (64.64646464646464, 35.35353535353536), (65.65656565656565, 34.343434343434346), (66.66666666666666, 33.333333333333336), (67.67676767676767, 32.323232323232325), (68.68686868686868, 31.313131313131315), (69.69696969696969, 30.303030303030305), (70.7070707070707, 29.292929292929294), (71.71717171717171, 28.282828282828284), (72.72727272727272, 27.272727272727273), (73.73737373737373, 26.262626262626263), (74.74747474747474, 25.252525252525253), (75.75757575757575, 24.242424242424242), (76.76767676767676, 23.232323232323235), (77.77777777777777, 22.222222222222225), (78.78787878787878, 21.212121212121215), (79.79797979797979, 20.202020202020204), (80.8080808080808, 19.191919191919194), (81.81818181818181, 18.181818181818183), (82.82828282828282, 17.171717171717173), (83.83838383838383, 16.161616161616163), (84.84848484848484, 15.151515151515152), (85.85858585858585, 14.141414141414142), (86.86868686868686, 13.131313131313131), (87.87878787878788, 12.121212121212121), (88.88888888888889, 11.111111111111112), (89.8989898989899, 10.101010101010102), (90.9090909090909, 9.090909090909092), (91.91919191919192, 8.080808080808081), (92.92929292929293, 7.070707070707071), (93.93939393939394, 6.0606060606060606), (94.94949494949495, 5.050505050505051), (95.95959595959596, 4.040404040404041), (96.96969696969697, 3.0303030303030303), (97.97979797979798, 2.0202020202020203), (98.98989898989899, 1.0101010101010102), (100.0, 0.0)], 'commodity': 'air'}, {}]
2016-09-29 10:14:34,935 (market-0.1 6123) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/electricity/offer/request [{'commodity': 'electricity'}, {}]
2016-09-29 10:14:34,965 (market-0.1 6123) market.agent INFO: Received Offer: abd22ce4-c0b6-4f5c-a694-bbde745f8b48 {'curve': [[0.0, 0.0], [100.0, 100.0]], 'type': 'SELL', 'commodity': 'electricity'}
2016-09-29 10:14:34,999 (market-0.1 5891) <stdout> INFO: AirMarket does not have enough SELL offers.
2016-09-29 10:14:35,004 (middleman-0.1 6006) middleman.agent INFO: Received Demand Curve Response: test/air/demandcurve/response {'curve': [[0.0, 100.0], [1.0101010101010104, 98.98989898989899], [2.0202020202020208, 97.97979797979798], [3.030303030303031, 96.96969696969697], [4.040404040404027, 95.95959595959597], [5.050505050505038, 94.94949494949496], [6.060606060606048, 93.93939393939395], [7.0707070707070585, 92.92929292929294], [8.080808080808069, 91.91919191919193], [9.09090909090908, 90.90909090909092], [10.10101010101009, 89.89898989898991], [11.1111111111111, 88.8888888888889], [12.12121212121211, 87.87878787878789], [13.13131313131312, 86.86868686868688], [14.141414141414131, 85.85858585858587], [15.151515151515142, 84.84848484848486], [16.161616161616152, 83.83838383838385], [17.171717171717162, 82.82828282828284], [18.181818181818173, 81.81818181818183], [19.191919191919183, 80.80808080808082], [20.202020202020194, 79.7979797979798], [21.212121212121204, 78.7878787878788], [22.222222222222214, 77.77777777777779], [23.232323232323225, 76.76767676767678], [24.242424242424235, 75.75757575757576], [25.252525252525245, 74.74747474747475], [26.262626262626256, 73.73737373737374], [27.272727272727266, 72.72727272727273], [28.282828282828277, 71.71717171717172], [29.292929292929287, 70.70707070707071], [30.303030303030297, 69.6969696969697], [31.313131313131308, 68.68686868686869], [32.32323232323232, 67.67676767676768], [33.33333333333333, 66.66666666666667], [34.34343434343434, 65.65656565656566], [35.35353535353535, 64.64646464646465], [36.36363636363636, 63.63636363636364], [37.37373737373737, 62.62626262626263], [38.38383838383838, 61.61616161616162], [39.39393939393939, 60.60606060606061], [40.4040404040404, 59.5959595959596], [41.41414141414141, 58.58585858585859], [42.42424242424242, 57.57575757575758], [43.43434343434343, 56.56565656565657], [44.44444444444444, 55.55555555555556], [45.45454545454545, 54.54545454545455], [46.464646464646464, 53.535353535353536], [47.474747474747474, 52.525252525252526], [48.484848484848484, 51.515151515151516], [49.494949494949495, 50.505050505050505], [50.505050505050505, 49.494949494949495], [51.515151515151516, 48.484848484848484], [52.52525252525252, 47.47474747474748], [53.53535353535353, 46.46464646464647], [54.54545454545454, 45.45454545454546], [55.55555555555555, 44.44444444444445], [56.56565656565656, 43.43434343434344], [57.57575757575757, 42.42424242424243], [58.58585858585858, 41.41414141414142], [59.59595959595959, 40.40404040404041], [60.6060606060606, 39.3939393939394], [61.61616161616161, 38.38383838383839], [62.62626262626262, 37.37373737373738], [63.63636363636363, 36.36363636363637], [64.64646464646464, 35.35353535353536], [65.65656565656565, 34.343434343434346], [66.66666666666666, 33.333333333333336], [67.67676767676767, 32.323232323232325], [68.68686868686868, 31.313131313131315], [69.69696969696969, 30.303030303030305], [70.7070707070707, 29.292929292929294], [71.71717171717171, 28.282828282828284], [72.72727272727272, 27.272727272727273], [73.73737373737373, 26.262626262626263], [74.74747474747474, 25.252525252525253], [75.75757575757575, 24.242424242424242], [76.76767676767676, 23.232323232323235], [77.77777777777777, 22.222222222222225], [78.78787878787878, 21.212121212121215], [79.79797979797979, 20.202020202020204], [80.8080808080808, 19.191919191919194], [81.81818181818181, 18.181818181818183], [82.82828282828282, 17.171717171717173], [83.83838383838383, 16.161616161616163], [84.84848484848484, 15.151515151515152], [85.85858585858585, 14.141414141414142], [86.86868686868686, 13.131313131313131], [87.87878787878788, 12.121212121212121], [88.88888888888889, 11.111111111111112], [89.8989898989899, 10.101010101010102], [90.9090909090909, 9.090909090909092], [91.91919191919192, 8.080808080808081], [92.92929292929293, 7.070707070707071], [93.93939393939394, 6.0606060606060606], [94.94949494949495, 5.050505050505051], [95.95959595959596, 4.040404040404041], [96.96969696969697, 3.0303030303030303], [97.97979797979798, 2.0202020202020203], [98.98989898989899, 1.0101010101010102], [100.0, 0.0]], 'commodity': 'air'}
2016-09-29 10:14:35,015 (middleman-0.1 6006) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/electricity/offer/response [{'curve': [(0.0, 100.0), (1.0101010101010104, 98.98989898989899), (2.0202020202020208, 97.97979797979798), (3.030303030303031, 96.96969696969697), (4.040404040404027, 95.95959595959597), (5.050505050505038, 94.94949494949496), (6.060606060606048, 93.93939393939395), (7.0707070707070585, 92.92929292929294), (8.080808080808069, 91.91919191919193), (9.09090909090908, 90.90909090909092), (10.10101010101009, 89.89898989898991), (11.1111111111111, 88.8888888888889), (12.12121212121211, 87.87878787878789), (13.13131313131312, 86.86868686868688), (14.141414141414131, 85.85858585858587), (15.151515151515142, 84.84848484848486), (16.161616161616152, 83.83838383838385), (17.171717171717162, 82.82828282828284), (18.181818181818173, 81.81818181818183), (19.191919191919183, 80.80808080808082), (20.202020202020194, 79.7979797979798), (21.212121212121204, 78.7878787878788), (22.222222222222214, 77.77777777777779), (23.232323232323225, 76.76767676767678), (24.242424242424235, 75.75757575757576), (25.252525252525245, 74.74747474747475), (26.262626262626256, 73.73737373737374), (27.272727272727266, 72.72727272727273), (28.282828282828277, 71.71717171717172), (29.292929292929287, 70.70707070707071), (30.303030303030297, 69.6969696969697), (31.313131313131308, 68.68686868686869), (32.32323232323232, 67.67676767676768), (33.33333333333333, 66.66666666666667), (34.34343434343434, 65.65656565656566), (35.35353535353535, 64.64646464646465), (36.36363636363636, 63.63636363636364), (37.37373737373737, 62.62626262626263), (38.38383838383838, 61.61616161616162), (39.39393939393939, 60.60606060606061), (40.4040404040404, 59.5959595959596), (41.41414141414141, 58.58585858585859), (42.42424242424242, 57.57575757575758), (43.43434343434343, 56.56565656565657), (44.44444444444444, 55.55555555555556), (45.45454545454545, 54.54545454545455), (46.464646464646464, 53.535353535353536), (47.474747474747474, 52.525252525252526), (48.484848484848484, 51.515151515151516), (49.494949494949495, 50.505050505050505), (50.505050505050505, 49.494949494949495), (51.515151515151516, 48.484848484848484), (52.52525252525252, 47.47474747474748), (53.53535353535353, 46.46464646464647), (54.54545454545454, 45.45454545454546), (55.55555555555555, 44.44444444444445), (56.56565656565656, 43.43434343434344), (57.57575757575757, 42.42424242424243), (58.58585858585858, 41.41414141414142), (59.59595959595959, 40.40404040404041), (60.6060606060606, 39.3939393939394), (61.61616161616161, 38.38383838383839), (62.62626262626262, 37.37373737373738), (63.63636363636363, 36.36363636363637), (64.64646464646464, 35.35353535353536), (65.65656565656565, 34.343434343434346), (66.66666666666666, 33.333333333333336), (67.67676767676767, 32.323232323232325), (68.68686868686868, 31.313131313131315), (69.69696969696969, 30.303030303030305), (70.7070707070707, 29.292929292929294), (71.71717171717171, 28.282828282828284), (72.72727272727272, 27.272727272727273), (73.73737373737373, 26.262626262626263), (74.74747474747474, 25.252525252525253), (75.75757575757575, 24.242424242424242), (76.76767676767676, 23.232323232323235), (77.77777777777777, 22.222222222222225), (78.78787878787878, 21.212121212121215), (79.79797979797979, 20.202020202020204), (80.8080808080808, 19.191919191919194), (81.81818181818181, 18.181818181818183), (82.82828282828282, 17.171717171717173), (83.83838383838383, 16.161616161616163), (84.84848484848484, 15.151515151515152), (85.85858585858585, 14.141414141414142), (86.86868686868686, 13.131313131313131), (87.87878787878788, 12.121212121212121), (88.88888888888889, 11.111111111111112), (89.8989898989899, 10.101010101010102), (90.9090909090909, 9.090909090909092), (91.91919191919192, 8.080808080808081), (92.92929292929293, 7.070707070707071), (93.93939393939394, 6.0606060606060606), (94.94949494949495, 5.050505050505051), (95.95959595959596, 4.040404040404041), (96.96969696969697, 3.0303030303030303), (97.97979797979798, 2.0202020202020203), (98.98989898989899, 1.0101010101010102), (100.0, 0.0)], 'type': 'BUY', 'commodity': 'electricity'}, {}]
2016-09-29 10:14:35,042 (market-0.1 6123) market.agent INFO: Received Offer: 290ec7a5-fd8f-486f-980b-9fc2fcb04db6 {'curve': [[0.0, 100.0], [1.0101010101010104, 98.98989898989899], [2.0202020202020208, 97.97979797979798], [3.030303030303031, 96.96969696969697], [4.040404040404027, 95.95959595959597], [5.050505050505038, 94.94949494949496], [6.060606060606048, 93.93939393939395], [7.0707070707070585, 92.92929292929294], [8.080808080808069, 91.91919191919193], [9.09090909090908, 90.90909090909092], [10.10101010101009, 89.89898989898991], [11.1111111111111, 88.8888888888889], [12.12121212121211, 87.87878787878789], [13.13131313131312, 86.86868686868688], [14.141414141414131, 85.85858585858587], [15.151515151515142, 84.84848484848486], [16.161616161616152, 83.83838383838385], [17.171717171717162, 82.82828282828284], [18.181818181818173, 81.81818181818183], [19.191919191919183, 80.80808080808082], [20.202020202020194, 79.7979797979798], [21.212121212121204, 78.7878787878788], [22.222222222222214, 77.77777777777779], [23.232323232323225, 76.76767676767678], [24.242424242424235, 75.75757575757576], [25.252525252525245, 74.74747474747475], [26.262626262626256, 73.73737373737374], [27.272727272727266, 72.72727272727273], [28.282828282828277, 71.71717171717172], [29.292929292929287, 70.70707070707071], [30.303030303030297, 69.6969696969697], [31.313131313131308, 68.68686868686869], [32.32323232323232, 67.67676767676768], [33.33333333333333, 66.66666666666667], [34.34343434343434, 65.65656565656566], [35.35353535353535, 64.64646464646465], [36.36363636363636, 63.63636363636364], [37.37373737373737, 62.62626262626263], [38.38383838383838, 61.61616161616162], [39.39393939393939, 60.60606060606061], [40.4040404040404, 59.5959595959596], [41.41414141414141, 58.58585858585859], [42.42424242424242, 57.57575757575758], [43.43434343434343, 56.56565656565657], [44.44444444444444, 55.55555555555556], [45.45454545454545, 54.54545454545455], [46.464646464646464, 53.535353535353536], [47.474747474747474, 52.525252525252526], [48.484848484848484, 51.515151515151516], [49.494949494949495, 50.505050505050505], [50.505050505050505, 49.494949494949495], [51.515151515151516, 48.484848484848484], [52.52525252525252, 47.47474747474748], [53.53535353535353, 46.46464646464647], [54.54545454545454, 45.45454545454546], [55.55555555555555, 44.44444444444445], [56.56565656565656, 43.43434343434344], [57.57575757575757, 42.42424242424243], [58.58585858585858, 41.41414141414142], [59.59595959595959, 40.40404040404041], [60.6060606060606, 39.3939393939394], [61.61616161616161, 38.38383838383839], [62.62626262626262, 37.37373737373738], [63.63636363636363, 36.36363636363637], [64.64646464646464, 35.35353535353536], [65.65656565656565, 34.343434343434346], [66.66666666666666, 33.333333333333336], [67.67676767676767, 32.323232323232325], [68.68686868686868, 31.313131313131315], [69.69696969696969, 30.303030303030305], [70.7070707070707, 29.292929292929294], [71.71717171717171, 28.282828282828284], [72.72727272727272, 27.272727272727273], [73.73737373737373, 26.262626262626263], [74.74747474747474, 25.252525252525253], [75.75757575757575, 24.242424242424242], [76.76767676767676, 23.232323232323235], [77.77777777777777, 22.222222222222225], [78.78787878787878, 21.212121212121215], [79.79797979797979, 20.202020202020204], [80.8080808080808, 19.191919191919194], [81.81818181818181, 18.181818181818183], [82.82828282828282, 17.171717171717173], [83.83838383838383, 16.161616161616163], [84.84848484848484, 15.151515151515152], [85.85858585858585, 14.141414141414142], [86.86868686868686, 13.131313131313131], [87.87878787878788, 12.121212121212121], [88.88888888888889, 11.111111111111112], [89.8989898989899, 10.101010101010102], [90.9090909090909, 9.090909090909092], [91.91919191919192, 8.080808080808081], [92.92929292929293, 7.070707070707071], [93.93939393939394, 6.0606060606060606], [94.94949494949495, 5.050505050505051], [95.95959595959596, 4.040404040404041], [96.96969696969697, 3.0303030303030303], [97.97979797979798, 2.0202020202020203], [98.98989898989899, 1.0101010101010102], [100.0, 0.0]], 'type': 'BUY', 'commodity': 'electricity'}
2016-09-29 10:14:35,058 (market-0.1 6123) <stdout> INFO: ElectricityMarket has enough BUY and SELL offers.
2016-09-29 10:14:35,076 (market-0.1 6123) <stdout> INFO: ElectricityMarket clears electricity at 50.0
2016-09-29 10:14:36,939 (director-0.1 6353) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/clear/request [{'clear': True}, {}]
2016-09-29 10:14:36,947 (seller-0.1 6238) pnnl.pubsubagent.pubsub.agent INFO: Received: test/electricity/clear/request [{'price': 50.00000000000006, 'commodity': 'electricity', 'quantity': 50.00000000000006}, {}]
2016-09-29 10:14:36,947 (middleman-0.1 6006) middleman.agent INFO: Received Buy Clear Request: test/electricity/clear/request {'price': 50.00000000000006, 'commodity': 'electricity', 'quantity': 50.00000000000006}
2016-09-29 10:14:36,947 (middleman-0.1 6006) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/air/offer/response [{'curve': [(0.0, 50.00000000000006), (100.0, 50.00000000000006)], 'type': 'SELL', 'commodity': 'air'}, {}]
2016-09-29 10:14:36,944 (market-0.1 6123) market.agent INFO: Received clear request from 10d96c00-7bf1-45d8-a199-9401c484cd1b
2016-09-29 10:14:36,944 (market-0.1 6123) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/electricity/clear/request [{'price': 50.00000000000006, 'commodity': 'electricity', 'quantity': 50.00000000000006}, {}]
2016-09-29 10:14:36,944 (market-0.1 5891) market.agent INFO: Received clear request from 10d96c00-7bf1-45d8-a199-9401c484cd1b
2016-09-29 10:14:36,950 (market-0.1 5891) market.agent INFO: Received Offer: 290ec7a5-fd8f-486f-980b-9fc2fcb04db6 {'curve': [[0.0, 50.00000000000006], [100.0, 50.00000000000006]], 'type': 'SELL', 'commodity': 'air'}
2016-09-29 10:14:36,953 (market-0.1 5891) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/air/clear/request [{'price': 50.00000000000006, 'commodity': 'air', 'quantity': 50.00000000000006}, {}]
2016-09-29 10:14:36,961 (market-0.1 5891) <stdout> INFO: AirMarket has enough BUY and SELL offers.
2016-09-29 10:14:36,961 (market-0.1 5891) <stdout> INFO: AirMarket clears air at 50.0
2016-09-29 10:14:36,963 (buyer-0.1 5776) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/shadeSchedule [1, {}]
2016-09-29 10:14:36,968 (buyer-0.1 5776) pnnl.pubsubagent.pubsub.agent INFO: Sending: test/extLightSchedule [1, {}]
2016-09-29 10:14:36,962 (middleman-0.1 6006) middleman.agent INFO: Received Sell Clear Request: test/air/clear/request {'price': 50.00000000000006, 'commodity': 'air', 'quantity': 50.00000000000006}
...
~~~

The market will be cleared every 5 seconds until the agents are stopped.

